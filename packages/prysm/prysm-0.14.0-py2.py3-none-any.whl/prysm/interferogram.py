"""tools to analyze interferometric data."""
import warnings

from .conf import config
from ._phase import OpticalPhase
from ._zernike import defocus
from .io import read_zygo_dat, read_zygo_datx
from .fttools import forward_ft_unit
from .coordinates import cart_to_polar, uniform_cart_to_polar
from .propagation import prop_pupil_plane_to_psf_plane
from .util import share_fig_ax
from .geometry import mcache


from prysm import mathops as m


class Interferogram(OpticalPhase):
    """Class containing logic and data for working with interferometric data."""
    def __init__(self, phase, intensity=None, x=None, y=None, scale='px', phase_unit='nm', meta=None):
        if x is None:  # assume x, y given together
            x = m.arange(phase.shape[1])
            y = m.arange(phase.shape[0])
            scale = 'px'
            self.lateral_res = 1

        wvl = meta.get('wavelength', None)
        if wvl is None:
            wvl = meta.get('Wavelength')

        if wvl is not None:
            wvl *= 1e6  # m to um

        super().__init__(unit_x=x, unit_y=y, phase=phase,
                         wavelength=wvl, phase_unit=phase_unit,
                         spatial_unit=scale)

        self.xaxis_label = 'X'
        self.yaxis_label = 'Y'
        self.zaxis_label = 'Height'
        self.intensity = intensity
        self.meta = meta

        if scale != 'px':
            self.change_spatial_unit(to=scale, inplace=True)

    @property
    def dropout_percentage(self):
        """Percentage of pixels in the data that are invalid (NaN)."""
        return m.count_nonzero(~m.isfinite(self.phase)) / self.phase.size * 100

    @property
    def pvr(self):
        """Peak-to-Valley residual.

        Notes
        -----

        See:
        C. Evans, "Robust Estimation of PV for Optical Surface Specification and Testing"
        in Optical Fabrication and Testing, OSA Technical Digest (CD)
        (Optical Society of America, 2008), paper OWA4.
        http://www.opticsinfobase.org/abstract.cfm?URI=OFT-2008-OWA4

        """
        from .fringezernike import fit, FringeZernike
        coefs, residual = fit(self.phase, terms=36, residual=True)
        fz = FringeZernike(coefs, samples=self.shape[0])
        return fz.pv + 3 * residual

    def fill(self, _with=0):
        """Fill invalid (NaN) values.

        Parameters
        ----------
        _with : `float`, optional
            value to fill with

        Returns
        -------
        `Interferogram`
            self

        """
        nans = ~m.isfinite(self.phase)
        self.phase[nans] = _with
        return self

    def crop(self):
        """Crop data to rectangle bounding non-NaN region."""
        nans = m.isfinite(self.phase)
        nancols = m.any(nans, axis=0)
        nanrows = m.any(nans, axis=1)

        left, right = nanrows.argmax(), nanrows[::-1].argmax()
        top, bottom = nancols.argmax(), nancols[::-1].argmax()
        if left == right == top == bottom == 0:
            return self

        self.phase = self.phase[left:-right, top:-bottom]
        self.unit_y, self.unit_x = self.unit_y[left:-right], self.unit_x[top:-bottom]
        self.unit_x -= self.unit_x[0]
        self.unit_y -= self.unit_y[0]
        return self

    def remove_piston(self):
        """Remove piston from the data by subtracting the mean value."""
        self.phase -= self.phase[m.isfinite(self.phase)].mean()
        return self

    def remove_tiptilt(self):
        """Remove tip/tilt from the data by least squares fitting and subtracting a plane."""
        plane = fit_plane(self.unit_x, self.unit_y, self.phase)
        self.phase -= plane
        return self

    def remove_power(self):
        """Remove power from the data by least squares fitting."""
        sphere = fit_sphere(self.phase)
        self.phase -= sphere
        return self

    def remove_piston_tiptilt(self):
        """Remove piston/tip/tilt from the data, see remove_tiptilt and remove_piston."""
        self.remove_piston()
        self.remove_tiptilt()
        return self

    def remove_piston_tiptilt_power(self):
        """Remove piston/tip/tilt/power from the data."""
        self.remove_piston()
        self.remove_piston_tiptilt()
        self.remove_power()
        return self

    def mask(self, shape=None, diameter=0, mask=None):
        """Mask the signal.

        The mask will be inscribed in the axis with fewer pixels.  I.e., for
        a interferogram with 1280x1000 pixels, the mask will be 1000x1000 at
        largest.

        Parameters
        ----------
        shape : `str`
            valid shape from prysm.geometry
        diameter : `float`
            diameter of the mask, in self.spatial_units
        mask : `numpy.ndarray`
            user-provided mask

        Returns
        -------
        self
            modified Interferogram instance.

        """
        if shape is None and mask is None:
            raise ValueError('must provide either a shape or a mask')

        if mask is None:
            mask = mcache(shape, min(self.shape), radius=diameter / min(self.diameter_x, self.diameter_y))
            base = m.zeros(self.shape, dtype=config.precision)
            difference = abs(self.shape[0] - self.shape[1])
            l, u = int(m.floor(difference / 2)), int(m.ceil(difference / 2))
            if u is 0:  # guard against nocrop scenario
                _slice = slice(None)
            else:
                _slice = slice(l, -u)
            if self.shape[0] < self.shape[1]:
                base[:, _slice] = mask
            else:
                base[_slice, :] = mask

            mask = base

        hitpts = mask == 0
        self.phase[hitpts] = m.nan
        return self

    def latcal(self, plate_scale, unit='mm'):
        """Perform lateral calibration.

        This probably won't do what you want if your data already has spatial
        units of anything but pixels (px).

        Parameters
        ----------
        plate_scale : `float`
            center-to-center sample spacing of pixels, in (unit)s.
        unit : `str`, optional
            unit associated with the plate scale.

        Returns
        -------
        self
            modified `Interferogram` instance.

        """
        self.change_spatial_unit(to=unit, inplace=True)  # will be 0..n spatial units
        # sloppy to do this here...
        self.unit_x *= plate_scale
        self.unit_y *= plate_scale
        return self

    def spike_clip(self, nsigma=3):
        """Clip points in the data that exceed a certain multiple of the standard deviation.

        Parameters
        ----------
        nsigma : `float`
            number of standard deviations to keep

        Returns
        -------
        self
            this Interferogram instance.

        """
        pts_over_nsigma = abs(self.phase) > nsigma * self.std
        self.phase[pts_over_nsigma] = m.nan
        return self

    def psd(self):
        """Power spectral density of the data., units (self.phase_unit^2)/((cy/self.spatial_unit)^2).

        Returns
        -------
        unit_x : `numpy.ndarray`
            ordinate x frequency axis
        unit_y : `numpy.ndarray`
            ordinate y frequency axis
        psd : `numpy.ndarray`
            power spectral density

        """
        return psd(self.phase, self.sample_spacing)

    def bandlimited_rms(self, wllow=None, wlhigh=None, flow=None, fhigh=None):
        """Calculate the bandlimited RMS of a signal from its PSD.

        Parameters
        ----------
        wllow : `float`
            short spatial scale
        wlhigh : `float`
            long spatial scale
        flow : `float`
            low frequency
        fhigh : `float`
            high frequency

        Returns
        -------
        `float`
            band-limited RMS value.

        """
        return bandlimited_rms(*self.psd(),
                               wllow=wllow,
                               wlhigh=wlhigh,
                               flow=flow,
                               fhigh=fhigh)

    def total_integrated_scatter(self, wavelength, incident_angle=0):
        """Calculate the total integrated scatter (TIS) for an angle or angles.

        Parameters
        ----------
        wavelength : `float`
            wavelength of light in microns.
        incident_angle : `float` or `numpy.ndarray`
            incident angle(s) of light.

        Returns
        -------
        `float` or `numpy.ndarray`
            TIS value.

        """
        if self.spatial_unit != 'μm':
            raise ValueError('Use microns for spatial unit when evaluating TIS.')

        upper_limit = 1 / wavelength
        kernel = 4 * m.pi * m.cos(m.radians(incident_angle))
        kernel *= self.bandlimited_rms(upper_limit, None) / wavelength
        return 1 - m.exp(-kernel**2)

    def psd_xy_avg(self):
        """Power spectral density of the data., units (self.phase_unit^2)/((cy/self.spatial_unit)^2).

        Returns
        -------
        `dict`
            with keys x, y, avg.  Each containing a tuple of (unit, psd)

        """
        x, y, _psd = self.psd()
        lx, ly = len(x)//2, len(y)//2

        rho, phi, _psdrp = uniform_cart_to_polar(x, y, _psd)

        return {
            'x': (x[lx:], _psd[ly, lx:]),
            'y': (y[ly:], _psd[ly:, lx]),
            'avg': (rho, _psdrp.mean(axis=0)),
        }

    def plot_psd2d(self, axlim=None, clim=(1e-9, 1e2), interp_method='lanczos', fig=None, ax=None):
        """Plot the two dimensional PSD.

        Parameters
        ----------
        axlim : `float`, optional
            symmetrical axis limit
        power : `float`, optional
            inverse of power to stretch image by
        interp_method : `str`, optional
            method used to interpolate the image, passed directly to matplotlib
            imshow
        fig : `matplotlib.figure.Figure`
            Figure containing the plot
        ax : `matplotlib.axes.Axis`
            Axis containing the plot

        Returns
        -------
        fig : `matplotlib.figure.Figure`
            Figure containing the plot
        ax : `matplotlib.axes.Axis`
            Axis containing the plot

        """
        from matplotlib import colors
        x, y, psd = self.psd()

        if axlim is None:
            lims = (None, None)
        else:
            lims = (-axlim, axlim)

        fig, ax = share_fig_ax(fig, ax)
        im = ax.imshow(psd,
                       extent=[x[0], x[-1], y[0], y[-1]],
                       origin='lower',
                       cmap='Greys_r',
                       norm=colors.LogNorm(*clim),
                       interpolation=interp_method)

        ax.set(xlim=lims, xlabel=r'$\nu_x$' + f' [cy/{self.spatial_unit}]',
               ylim=lims, ylabel=r'$\nu_y$' + f' [cy/{self.spatial_unit}]')

        cb = fig.colorbar(im,
                          label='PSD [' + self.phase_unit + r'$^2$' + f'/(cy/{self.spatial_unit})]',
                          ax=ax, fraction=0.046, extend='both')
        cb.outline.set_edgecolor('k')
        cb.outline.set_linewidth(0.5)

        return fig, ax

    def plot_psd_xy_avg(self, a=None, b=None, c=None, lw=3,
                       xlim=None, ylim=None, fig=None, ax=None):
        """Plot the x, y, and average PSD on a linear x axis.

        Parameters
        ----------
        a : `float`, optional
            a coefficient of Lorentzian PSD model plotted alongside data
        b : `float`, optional
            b coefficient of Lorentzian PSD model plotted alongside data
        c : `float`, optional
            c coefficient of Lorentzian PSD model plotted alongside data
        lw : `float`, optional
            linewidth provided directly to matplotlib
        xlim : `tuple`, optional
            len 2 tuple of low, high x axis limits
        ylim : `tuple`, optional
            len 2 tuple of low, high y axis limits
        fig : `matplotlib.figure.Figure`
            Figure containing the plot
        ax : `matplotlib.axes.Axis`
            Axis containing the plot

        Returns
        -------
        fig : `matplotlib.figure.Figure`
            Figure containing the plot
        ax : `matplotlib.axes.Axis`
            Axis containing the plot

        Notes
        -----
        if a, b given but not c, an AB / inverse power model will be used for the PSD.
        If a, b, c are given the Lorentzian model will be used.

        """
        xyavg = self.psd_xy_avg()
        x, px = xyavg['x']
        y, py = xyavg['y']
        r, pr = xyavg['avg']

        fig, ax = share_fig_ax(fig, ax)
        ax.loglog(x, px, lw=lw, label='x', alpha=0.4)
        ax.loglog(y, py, lw=lw, label='y', alpha=0.4)
        ax.loglog(r, pr, lw=lw*1.5, label='avg')

        if a is not None:
            if c is not None:
                requirement = abc_psd(a=a, b=b, c=c, nu=r)
            else:
                requirement = ab_psd(a=a, b=b, nu=r)
            ax.loglog(r, requirement, c='k', lw=lw*2)

        ax.legend(title='Orientation')
        ax.set(xlim=xlim, xlabel=f'Spatial Frequency [cy/{self.spatial_unit}]',
               ylim=ylim, ylabel=r'PSD [nm$^2$/' + f'(cy/{self.spatial_unit})$^2$]')

        return fig, ax

    @staticmethod
    def from_zygo_dat(path, multi_intensity_action='first', scale='mm'):
        """Create a new interferogram from a zygo dat file.

        Parameters
        ----------
        path : path_like
            path to a zygo dat file
        multi_intensity_action : str, optional
            see `io.read_zygo_dat`
        scale : `str`, optional, {'um', 'mm'}
            what xy scale to label the data with, microns or mm

        Returns
        -------
        `Interferogram`
            new Interferogram instance

        """
        if str(path).endswith('datx'):
            # datx file, use datx reader
            zydat = read_zygo_datx(path)
            res = zydat['meta']['Lateral Resolution']
        else:
            # dat file, use dat file reader
            zydat = read_zygo_dat(path, multi_intensity_action=multi_intensity_action)
            res = zydat['meta']['lateral_resolution']  # meters

        phase = zydat['phase']
        if res == 0.0:
            res = 1
            scale = 'px'

        if scale != 'px':
            _scale = 'm'
        else:
            _scale = 'px'

        i = Interferogram(phase=phase, intensity=zydat['intensity'],
                          x=m.arange(phase.shape[1]) * res, y=m.arange(phase.shape[0]) * res,
                          scale=_scale, meta=zydat['meta'])
        return i.change_spatial_unit(to=scale.lower(), inplace=True)


def fit_plane(x, y, z):
    xx, yy = m.meshgrid(x, y)
    pts = m.isfinite(z)
    xx_, yy_ = xx[pts].flatten(), yy[pts].flatten()
    flat = m.ones(xx_.shape)

    coefs = m.lstsq(m.stack([xx_, yy_, flat]).T, z[pts].flatten(), rcond=None)[0]
    plane_fit = coefs[0] * xx + coefs[1] * yy + coefs[2]
    return plane_fit


def fit_sphere(z):
    x, y = m.linspace(-1, 1, z.shape[1]), m.linspace(-1, 1, z.shape[0])
    xx, yy = m.meshgrid(x, y)
    pts = m.isfinite(z)
    xx_, yy_ = xx[pts].flatten(), yy[pts].flatten()
    rho, phi = cart_to_polar(xx_, yy_)
    focus = defocus(rho, phi)

    coefs = m.lstsq(m.stack([focus, m.ones(focus.shape)]).T, z[pts].flatten(), rcond=None)[0]
    rho, phi = cart_to_polar(xx, yy)
    sphere = defocus(rho, phi) * coefs[0]
    return sphere


def make_window(signal, sample_spacing, which='welch'):
    """Generates a window function to be used in PSD analysis.

    Parameters
    ----------
    signal : `numpy.ndarray`
        signal or phase data
    sample_spacing : `float`
        spacing of samples in the input data
    which : `str,` {'welch', 'hann', 'auto'}, optional
        which window to produce.  If auto, attempts to guess the appropriate
        window based on the input signal

    Notes
    -----
    For 2D welch, see:
    Power Spectral Density Specification and Analysis of Large Optical Surfaces
    E. Sidick, JPL

    Returns
    -------
    `numpy.ndarray`
        window array

    """
    s = signal.shape

    if which is None:
        # attempt to guess best window
        ysamples = int(round(s[0] * 0.02, 0))
        xsamples = int(round(s[1] * 0.02, 0))
        corner1 = signal[:ysamples, :xsamples] == 0
        corner2 = signal[-ysamples:, :xsamples] == 0
        corner3 = signal[:ysamples, -xsamples:] == 0
        corner4 = signal[-ysamples:, -xsamples:] == 0
        if corner1.all() and corner2.all() and corner3.all() and corner4.all():
            # four corners all "black" -- circular data, Welch window is best
            # looks wrong but 2D welch takes x, y while indices are y, x
            y = m.arange(s[1]) * sample_spacing
            x = m.arange(s[0]) * sample_spacing
            return window_2d_welch(y, x)
        else:
            # if not circular, square data; use Hanning window
            y = m.hanning(s[0])
            x = m.hanning(s[1])
            return m.outer(y, x)
    else:
        if type(which) is str:
            # known window type
            wl = which.lower()
            if wl == 'welch':
                y = m.arange(s[1]) * sample_spacing
                x = m.arange(s[0]) * sample_spacing
                return window_2d_welch(y, x)
            elif wl in ('hann', 'hanning'):
                y = m.hanning(s[0])
                x = m.hanning(s[1])
                return m.outer(y, x)
            else:
                raise ValueError('unknown window type')
        else:
            return which  # window provided as ndarray


def psd(height, sample_spacing, window=None):
    """Compute the power spectral density of a signal.

    Parameters
    ----------
    height : `numpy.ndarray`
        height or phase data
    sample_spacing : `float`
        spacing of samples in the input data
    window : {'welch', 'hann'} or ndarray, optional

    Returns
    -------
    unit_x : `numpy.ndarray`
        ordinate x frequency axis
    unit_y : `numpy.ndarray`
        ordinate y frequency axis
    psd : `numpy.ndarray`
        power spectral density

    Notes
    -----
    See GH_FFT for a rigorous treatment of FFT scalings
    https://holometer.fnal.gov/GH_FFT.pdf

    """
    window = make_window(height, sample_spacing, window)
    fft = m.ifftshift(m.fft2(m.fftshift(height * window)))
    psd = abs(fft)**2  # mag squared first as per GH_FFT

    fs = 1 / sample_spacing
    S2 = (window**2).sum()
    coef = S2 * fs * fs
    psd /= coef

    ux = forward_ft_unit(sample_spacing, height.shape[1])
    uy = forward_ft_unit(sample_spacing, height.shape[0])
    return ux, uy, psd


def bandlimited_rms(ux, uy, psd, wllow=None, wlhigh=None, flow=None, fhigh=None):
    """Calculate the bandlimited RMS of a signal from its PSD.

    Parameters
    ----------
    ux : `numpy.ndarray`
        x spatial frequencies
    uy : `numpy.ndarray`
        y spatial frequencies
    psd : `numpy.ndarray`
        power spectral density
    wllow : `float`
        short spatial scale
    wlhigh : `float`
        long spatial scale
    flow : `float`
        low frequency
    fhigh : `float`
        high frequency

    Returns
    -------
    `float`
        band-limited RMS value.

    """
    if wllow is not None or wlhigh is not None:
        # spatial period given
        if wllow is None:
            flow = 0
        else:
            fhigh = 1 / wllow

        if wlhigh is None:
            fhigh = max(ux[-1], uy[-1])
        else:
            flow = 1 / wlhigh
    elif flow is not None or fhigh is not None:
        # spatial frequency given
        if flow is None:
            flow = 0
        if fhigh is None:
            fhigh = max(ux[-1], uy[-1])
    else:
        raise ValueError('must specify either period (wavelength) or frequency')

    ux2, uy2 = m.meshgrid(ux, uy)
    r, p = cart_to_polar(ux2, uy2)

    if flow is None:
        warnings.warn('no lower limit given, using 0 for low frequency')
        flow = 0

    if fhigh is None:
        warnings.warn('no upper limit given, using limit imposed by data.')
        fhigh = r.max()

    work = psd.copy()
    work[r < flow] = 0
    work[r > fhigh] = 0
    first = m.trapz(work, uy, axis=0)
    second = m.trapz(first, ux, axis=0)
    return m.sqrt(second)


def window_2d_welch(x, y, alpha=8):
    """Return a 2D welch window for a given alpha.

    Parameters
    ----------
    x : `numpy.ndarray`
        x values, 1D array
    y : `numpy.ndarray`
        y values, 1D array
    alpha : `float`
        alpha (edge roll) parameter

    Returns
    -------
    `numpy.ndarray`
        window

    """
    xx, yy = m.meshgrid(x, y)
    r, _ = cart_to_polar(xx, yy)
    rmax = m.sqrt(x.max()**2 + y.max()**2)
    window = 1 - abs(r/rmax)**alpha
    return window


def abc_psd(nu, a, b, c):
    """Lorentzian model of a Power Spectral Density.

    Parameters
    ----------
    nu : `numpy.ndarray` or `float`
        spatial frequency
    a : `float`
        a coefficient
    b : `float`
        b coefficient
    c : `float`
        c coefficient

    Returns
    -------
    `numpy.ndarray`
        value of PSD model

    """
    return a / (1 + (nu/b)**2)**(c/2)


def ab_psd(nu, a, b):
    """inverse power model of a Power Spectral Density.

    Parameters
    ----------
    nu : `numpy.ndarray` or `float`
        spatial frequency
    a : `float`
        a coefficient
    b : `float`
        b coefficient

    Returns
    -------
    `numpy.ndarray`
        value of PSD model

    """
    return a * nu ** (-b)
