"""
    Class for grids of the three components of the magnetic field, the
    magnetic intensity, and the magnetic potential.
"""
import matplotlib as _mpl
import matplotlib.pyplot as _plt
import copy as _copy
import xarray as _xr

from .shcoeffsgrid import SHGrid as _SHGrid


class SHMagGrid(object):
    """
    Class for grids of the magnetic potential, three vector components of
    the magnetic field, and the total magnetic intensity. The class is
    initialized from a class instance of SHMagCoeffs using the method
    expand().

    Attributes:

    rad            : SHGrid class instance of the radial component of the
                     magnetic field evaluated on an ellipsoid.
    theta          : SHGrid class instance of the theta component of the
                     magnetic field evaluated on an ellipsoid.
    phi            : SHGrid class instance of the phi component of the
                     magnetic field evaluated on an ellipsoid.
    total          : SHGrid class instance of the total magnetic intensity on
                     an ellipsoid.
    pot            : SHGrid class instance of the magnetic potential
                     evaluated on an ellipsoid.
    a              : Semimajor axis of the reference ellipsoid.
    f              : Flattening of the reference ellipsoid, f=(a-b)/a.
    lmax           : The maximum spherical harmonic degree resolvable by the
                     grids.
    lmax_calc      : The maximum spherical harmonic degree of the magnetic
                     potential used in creating the grids.
    nlat, nlon     : The number of latitude and longitude bands in the grids.
    n              : The number of samples in latitude.
    sampling       : The longitudinal sampling for Driscoll and Healy grids.
                     Either 1 for equally sampled grids (nlat=nlon) or 2 for
                     equally spaced grids in degrees.
    extend         : True if the grid contains the redundant column for 360 E
                     and the unnecessary row for 90 S.

    Methods:

    plot()        : Plot all three components of the magnetic field and the
                    total magnetic intensity.
    plot_rad()    : Plot the radial component of the magnetic field.
    plot_theta()  : Plot the theta component of the magnetic field.
    plot_phi()    : Plot the phi component of the magnetic field.
    plot_total()  : Plot the total magnetic intensity.
    plot_pot()    : Plot the magnetic potential.
    to_xarray()   : Return an xarray DataSet of all gridded data.
    copy()        : Return a copy of the class instance.
    info()        : Print a summary of the data stored in the SHMagGrid
                    instance.
    """

    def __init__(self, rad, theta, phi, total, pot, a, f, lmax, lmax_calc):
        """
        Initialize the SHMagGrid class.
        """
        self.rad = _SHGrid.from_array(rad, grid='DH')
        self.theta = _SHGrid.from_array(theta, grid='DH')
        self.phi = _SHGrid.from_array(phi, grid='DH')
        self.total = _SHGrid.from_array(total, grid='DH')
        self.pot = _SHGrid.from_array(pot, grid='DH')
        self.grid = self.rad.grid
        self.sampling = self.rad.sampling
        self.nlat = self.rad.nlat
        self.nlon = self.rad.nlon
        self.n = self.rad.n
        self.extend = self.rad.extend
        self.a = a
        self.f = f
        self.lmax = lmax
        self.lmax_calc = lmax_calc

    def copy(self):
        """
        Return a deep copy of the class instance.

        Usage
        -----
        copy = x.copy()
        """
        return _copy.deepcopy(self)

    def info(self):
        """
        Print a summary of the data stored in the SHMagGrid class instance.

        Usage
        -----
        x.info()
        """
        print(repr(self))

    def __repr__(self):
        str = ('grid = {:s}\n'
               'nlat = {:d}\n'
               'nlon = {:d}\n'
               'n = {:d}\n'
               'sampling = {:d}\n'
               'extend = {}\n'
               'lmax = {:d}\n'
               'lmax_calc = {:d}\n'
               'a (m)= {:e}\n'
               'f = {:e}'
               .format(self.grid, self.nlat, self.nlon, self.n, self.sampling,
                       self.extend, self.lmax, self.lmax_calc, self.a, self.f))
        return str

    def plot_rad(self, projection=None, tick_interval=[30, 30],
                 minor_tick_interval=[None, None], xlabel=None, ylabel=None,
                 title=None, titlesize=None, colorbar='vertical',
                 cmap='viridis', cmap_limits=None, cmap_reverse=False,
                 cb_triangles='neither', cb_label='$B_r$, nT',
                 cb_tick_interval=None, grid=False, axes_labelsize=None,
                 tick_labelsize=None, show=True, ax=None,
                 fname=None):
        """
        Plot the radial component of the magnetic field.

        Usage
        -----
        x.plot_rad([projection, tick_interval, minor_tick_interval, xlabel,
                    ylabel, title, colorbar, cmap, cmap_limits, cmap_reverse,
                    cb_triangles, cb_label, cb_tick_interval, grid, titlesize,
                    axes_labelsize, tick_labelsize, ax, show, fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [30, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        title : str or list, optional, default = None
            The title of the plot.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_label : str, optional, default = '$B_r$, nT'
            Text label for the colorbar.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        titlesize : int, optional, default = None
            The font size of the title.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        return self.rad.plot(projection=projection,
                             tick_interval=tick_interval,
                             minor_tick_interval=minor_tick_interval,
                             xlabel=xlabel, ylabel=ylabel, title=title,
                             titlesize=titlesize, colorbar=colorbar,
                             cmap=cmap, cmap_limits=cmap_limits,
                             cmap_reverse=cmap_reverse,
                             cb_triangles=cb_triangles, cb_label=cb_label,
                             cb_tick_interval=cb_tick_interval, grid=grid,
                             axes_labelsize=axes_labelsize,
                             tick_labelsize=tick_labelsize, ax=ax,
                             show=show, fname=fname)

    def plot_theta(self, projection=None, tick_interval=[30, 30],
                   minor_tick_interval=[None, None], xlabel=None, ylabel=None,
                   title=None, titlesize=None, colorbar='vertical',
                   cmap='viridis', cmap_limits=None, cmap_reverse=False,
                   cb_triangles='neither', cb_label='$B_\\theta$, nT',
                   cb_tick_interval=None, grid=False, axes_labelsize=None,
                   tick_labelsize=None, show=True, ax=None,
                   fname=None):
        """
        Plot the theta component of the magnetic field.

        Usage
        -----
        x.plot_theta([projection, tick_interval, minor_tick_interval, xlabel,
                      ylabel, title, colorbar, cmap, cmap_limits, cmap_reverse,
                      cb_triangles, cb_label, cb_tick_interval, grid,
                      titlesize, axes_labelsize, tick_labelsize, ax, show,
                      fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [30, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        title : str or list, optional, default = None
            The title of the plot.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_label : str, optional, default = '$B_\\theta$, nT'
            Text label for the colorbar.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        titlesize : int, optional, default = None
            The font size of the title.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        return self.theta.plot(projection=projection,
                               tick_interval=tick_interval,
                               minor_tick_interval=minor_tick_interval,
                               xlabel=xlabel, ylabel=ylabel, title=title,
                               titlesize=titlesize, colorbar=colorbar,
                               cmap=cmap, cmap_limits=cmap_limits,
                               cmap_reverse=cmap_reverse,
                               cb_triangles=cb_triangles, cb_label=cb_label,
                               cb_tick_interval=cb_tick_interval, grid=grid,
                               axes_labelsize=axes_labelsize,
                               tick_labelsize=tick_labelsize, ax=ax,
                               show=show, fname=fname)

    def plot_phi(self, projection=None, tick_interval=[30, 30],
                 minor_tick_interval=[None, None], xlabel=None, ylabel=None,
                 title=None, titlesize=None, colorbar='vertical',
                 cmap='viridis', cmap_limits=None, cmap_reverse=False,
                 cb_triangles='neither', cb_label='$B_\phi$, nT',
                 cb_tick_interval=None, grid=False, axes_labelsize=None,
                 tick_labelsize=None, show=True, ax=None,
                 fname=None):
        """
        Plot the phi component of the magnetic field.

        Usage
        -----
        x.plot_phi([projection, tick_interval, minor_tick_interval, xlabel,
                    ylabel, title, colorbar, cmap, cmap_limits, cmap_reverse,
                    cb_triangles, cb_label, cb_tick_interval, grid, titlesize,
                    axes_labelsize, tick_labelsize, ax, show, fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [30, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        title : str or list, optional, default = None
            The title of the plot.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_label : str, optional, default = '$B_\phi$, nT'
            Text label for the colorbar.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        titlesize : int, optional, default = None
            The font size of the title.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        return self.phi.plot(projection=projection,
                             tick_interval=tick_interval,
                             minor_tick_interval=minor_tick_interval,
                             xlabel=xlabel, ylabel=ylabel, title=title,
                             titlesize=titlesize, colorbar=colorbar,
                             cmap=cmap, cmap_limits=cmap_limits,
                             cmap_reverse=cmap_reverse,
                             cb_triangles=cb_triangles, cb_label=cb_label,
                             cb_tick_interval=cb_tick_interval, grid=grid,
                             axes_labelsize=axes_labelsize,
                             tick_labelsize=tick_labelsize, ax=ax,
                             show=show, fname=fname)

    def plot_total(self, projection=None, tick_interval=[30, 30],
                   minor_tick_interval=[None, None], xlabel=None, ylabel=None,
                   title=None, titlesize=None, colorbar='vertical',
                   cmap='viridis', cmap_limits=None, cmap_reverse=False,
                   cb_triangles='neither', cb_label='$|B|$, nT',
                   cb_tick_interval=None, grid=False, axes_labelsize=None,
                   tick_labelsize=None, show=True, ax=None,
                   fname=None):
        """
        Plot the total magnetic intensity.

        Usage
        -----
        x.plot_total([projection, tick_interval, minor_tick_interval, xlabel,
                      ylabel, title, colorbar, cmap, cmap_limits, cmap_reverse,
                      cb_triangles, cb_label, cb_tick_interval, grid,
                      titlesize, axes_labelsize, tick_labelsize, ax, show,
                      fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [30, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        title : str or list, optional, default = None
            The title of the plot.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_label : str, optional, default = '$|B|$, nT'
            Text label for the colorbar.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        titlesize : int, optional, default = None
            The font size of the title.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        return self.total.plot(projection=projection,
                               tick_interval=tick_interval,
                               minor_tick_interval=minor_tick_interval,
                               xlabel=xlabel, ylabel=ylabel, title=title,
                               titlesize=titlesize, colorbar=colorbar,
                               cmap=cmap, cmap_limits=cmap_limits,
                               cmap_reverse=cmap_reverse,
                               cb_triangles=cb_triangles, cb_label=cb_label,
                               cb_tick_interval=cb_tick_interval, grid=grid,
                               axes_labelsize=axes_labelsize,
                               tick_labelsize=tick_labelsize, ax=ax,
                               show=show, fname=fname)

    def plot_pot(self, projection=None, tick_interval=[30, 30],
                 minor_tick_interval=[None, None], xlabel=None, ylabel=None,
                 title=None, titlesize=None, colorbar='vertical',
                 cmap='viridis', cmap_limits=None, cmap_reverse=False,
                 cb_triangles='neither', cb_label='Potential, nT m',
                 cb_tick_interval=None, grid=False, axes_labelsize=None,
                 tick_labelsize=None, show=True, ax=None,
                 fname=None):
        """
        Plot the gravitational potential.

        Usage
        -----
        x.plot_pot([projection, tick_interval, minor_tick_interval, xlabel,
                    ylabel, title, colorbar, cmap, cmap_limits, cmap_reverse,
                    cb_triangles, cb_label, cb_tick_interval, grid, titlesize,
                    axes_labelsize, tick_labelsize, ax, show, fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [30, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        title : str or list, optional, default = None
            The title of the plot.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_label : str, optional, default = 'Potential, nT m'
            Text label for the colorbar.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        titlesize : int, optional, default = None
            The font size of the title.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        return self.pot.plot(projection=projection,
                             tick_interval=tick_interval,
                             minor_tick_interval=minor_tick_interval,
                             xlabel=xlabel, ylabel=ylabel, title=title,
                             titlesize=titlesize, colorbar=colorbar,
                             cmap=cmap, cmap_limits=cmap_limits,
                             cmap_reverse=cmap_reverse,
                             cb_triangles=cb_triangles, cb_label=cb_label,
                             cb_tick_interval=cb_tick_interval, grid=grid,
                             axes_labelsize=axes_labelsize,
                             tick_labelsize=tick_labelsize, ax=ax,
                             show=show, fname=fname)

    def plot(self, projection=None, tick_interval=[60, 30],
             minor_tick_interval=[None, None], xlabel='Longitude',
             ylabel='Latitude', colorbar='horizontal', cmap='viridis',
             cmap_limits=None, cmap_reverse=False, cb_triangles='neither',
             cb_tick_interval=None, grid=False, axes_labelsize=9,
             tick_labelsize=8, show=True, ax=None, fname=None):
        """
        Plot the three vector components of the magnetic field and total
        intensity.

        Usage
        -----
        x.plot([projection, tick_interval, minor_tick_interval, xlabel,
                ylabel, colorbar, cmap, cmap_limits, cmap_reverse,
                cb_triangles, cb_tick_interval, grid, axes_labelsize,
                tick_labelsize, ax, show, fname])

        Parameters
        ----------
        projection : Cartopy projection class, optional, default = None
            The Cartopy projection class used to project the gridded data,
            for Driscoll and Healy sampled grids only.
        tick_interval : list or tuple, optional, default = [60, 30]
            Intervals to use when plotting the x and y ticks. If set to None,
            ticks will not be plotted.
        minor_tick_interval : list or tuple, optional, default = [None, None]
            Intervals to use when plotting the minor x and y ticks. If set to
            None, minor ticks will not be plotted.
        xlabel : str, optional, default = 'longitude'
            Label for the longitude axis.
        ylabel : str, optional, default = 'latitude'
            Label for the latitude axis.
        colorbar : str, optional, default = None
            Plot a colorbar that is either 'horizontal' or 'vertical'.
        cmap : str, optional, default = 'viridis'
            The color map to use when plotting the data and colorbar.
        cmap_limits : list, optional, default = [self.min(), self.max()]
            Set the lower and upper limits of the data used by the colormap,
            and optionally an interval for each color band. If the interval is
            specified, the number of discrete colors will be
            (cmap_limits[1]-cmap_limits[0])/cmap_limits[2].
        cmap_reverse : bool, optional, default = False
            Set to True to reverse the sense of the color progression in the
            color table.
        cb_triangles : str, optional, default = 'neither'
            Add triangles to the edges of the colorbar for minimum and maximum
            values. Can be 'neither', 'both', 'min', or 'max'.
        cb_tick_interval : float, optional, default = None
            Colorbar tick interval.
        grid : bool, optional, default = False
            If True, plot major grid lines.
        axes_labelsize : int, optional, default = None
            The font size for the x and y axes labels.
        tick_labelsize : int, optional, default = None
            The font size for the x and y tick labels.
        ax : matplotlib axes object, optional, default = None
            A single matplotlib axes object where the plot will appear.
        show : bool, optional, default = True
            If True, plot the image to the screen.
        fname : str, optional, default = None
            If present, and if axes is not specified, save the image to the
            specified file.
        """
        if colorbar is not None:
            if colorbar == 'horizontal':
                scale = 0.8
            elif colorbar == 'vertical':
                scale = 0.5
            else:
                raise ValueError("colorbar must be either 'horizontal' or "
                                 "'vertical'. Input value is {:s}."
                                 .format(repr(colorbar)))
        else:
            scale = 0.6
        figsize = (_mpl.rcParams['figure.figsize'][0],
                   _mpl.rcParams['figure.figsize'][0] * scale)

        fig, ax = _plt.subplots(2, 2, figsize=figsize)
        self.plot_rad(projection=projection, ax=ax.flat[0],
                      tick_interval=tick_interval,
                      minor_tick_interval=minor_tick_interval,
                      xlabel=xlabel, ylabel=ylabel, title=None,
                      titlesize=None, colorbar=colorbar,
                      cmap=cmap, cmap_limits=cmap_limits,
                      cmap_reverse=cmap_reverse, cb_triangles=cb_triangles,
                      cb_tick_interval=cb_tick_interval,
                      grid=grid, axes_labelsize=axes_labelsize,
                      tick_labelsize=tick_labelsize,
                      show=show, fname=None)
        self.plot_theta(projection=projection, ax=ax.flat[1],
                        tick_interval=tick_interval,
                        minor_tick_interval=minor_tick_interval,
                        xlabel=xlabel, ylabel=ylabel, title=None,
                        titlesize=None, colorbar=colorbar,
                        cmap=cmap, cmap_limits=cmap_limits,
                        cmap_reverse=cmap_reverse, cb_triangles=cb_triangles,
                        cb_tick_interval=cb_tick_interval,
                        grid=grid, axes_labelsize=axes_labelsize,
                        tick_labelsize=tick_labelsize,
                        show=show, fname=None)
        self.plot_phi(projection=projection, ax=ax.flat[2],
                      tick_interval=tick_interval,
                      minor_tick_interval=minor_tick_interval,
                      xlabel=xlabel, ylabel=ylabel, title=None,
                      titlesize=None, colorbar=colorbar,
                      cmap=cmap, cmap_limits=cmap_limits,
                      cmap_reverse=cmap_reverse, cb_triangles=cb_triangles,
                      cb_tick_interval=cb_tick_interval,
                      grid=grid, axes_labelsize=axes_labelsize,
                      tick_labelsize=tick_labelsize,
                      show=show, fname=None)
        self.plot_total(projection=projection, ax=ax.flat[3],
                        tick_interval=tick_interval,
                        minor_tick_interval=minor_tick_interval,
                        xlabel=xlabel, ylabel=ylabel, title=None,
                        titlesize=None, colorbar=colorbar,
                        cmap=cmap, cmap_limits=cmap_limits,
                        cmap_reverse=cmap_reverse, cb_triangles=cb_triangles,
                        cb_tick_interval=cb_tick_interval,
                        grid=grid, axes_labelsize=axes_labelsize,
                        tick_labelsize=tick_labelsize,
                        show=show, fname=None)
        fig.tight_layout(pad=0.5)

        if fname is not None:
            fig.savefig(fname)
        return fig, ax

    def to_xarray(self, title='', description='',
                  comment='pyshtools grid'):
        """
        Return the magnetic field gridded data as an xarray DataSet.

        Usage
        -----
        x.to_xarray([title, description, comment])

        Parameters
        ----------
        title : str, optional, default = ''
            Title of the dataset.
        description : str, optional, default = ''
            Description of the dataset ('Remark' in gmt grd files).
        comment : str, optional, default = 'pyshtools grid'
            Additional information about how the data were generated.
        """
        attrs = {'title': title,
                 'description': description,
                 'comment': comment,
                 'nlat': self.nlat,
                 'nlon': self.nlon,
                 'lmax': self.lmax,
                 'grid': self.grid,
                 'a': self.a,
                 'f': self.f,
                 'lmax_calc': self.lmax_calc,
                 'sampling': self.sampling,
                 'n': self.n,
                 'extend': self.extend
                 }

        _total = self.total.to_xarray(title='magnetic field intensity',
                                      long_name='$|B|$', units='$nT$')
        _rad = self.rad.to_xarray(title='magnetic field (radial)',
                                  long_name='$B_r$', units='$nT$')
        _theta = self.theta.to_xarray(title='magnetic field (theta)',
                                      long_name='$B_\\theta$', units='$nT$')
        _phi = self.phi.to_xarray(title='magnetic field (phi)',
                                  long_name='$B_\\phi$', units='$nT$')
        _pot = self.pot.to_xarray(title='magnetic field potential',
                                  long_name='potential', units='$m nT$')

        return _xr.Dataset({'radial': _rad, 'theta': _theta, 'phi': _phi,
                            'total': _total, 'potential': _pot}, attrs=attrs)
