from matplotlib.figure import Figure
from matplotlib.pyplot import figure as pyplot_fig
from matplotlib.ticker import EngFormatter, AutoMinorLocator
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes

def set_ax_format(ax):
    """Set axis number labels to engineering format and set tick locations
    """
    # Define axis labels format
    format_eng = EngFormatter(places=1, unit=" ", sep="\N{THIN SPACE}")
    # ticks_log_E6 = ticker.LogLocator(subs=(1.0, 1.5, 2.2, 3.3, 4.7, 6.8))
    ax.set_tick_params(which="major", length=6.0)
    # axis ticks and labels
    ax.set_major_formatter(format_eng)
    ax.set_minor_locator(AutoMinorLocator())

def plot_3_axes(
        ax1_color: str = "red",
        ax2_color: str = "green",
        ax3_color: str = "blue",
        figure = None
        ) -> tuple[Figure, HostAxes, ParasiteAxes, ParasiteAxes]:
    """Plot three individually auto-scaled sets of data on a single X-axis
    
    First Y-axis is located on the left side of the plot,
    second and third Y-axes are placed on the right hand side.
    """
    if figure is None:
        figure = pyplot_fig()
    host_ax = figure.add_subplot(axes_class=HostAxes)
    par_ax1 = host_ax.twinx()
    par_ax2 = host_ax.twinx()
    # Format axis number labels and ticks
    for axis in (host_ax.xaxis, host_ax.yaxis, par_ax1.yaxis, par_ax2.yaxis):
        set_ax_format(axis)
    # Y axes are AxisArtist instances
    yart1 = host_ax.axis["left"]
    yart2 = par_ax1.axis["right"]
    # Offset axis to replace original AxisArtist
    yart3 = par_ax2.new_fixed_axis(loc="right", offset=(65, 0))
    par_ax2.axis["right"] = yart3
    # Configure all Y axes
    yart2.toggle(all=True)
    yart3.toggle(all=True)
    yart1.label.set_color(ax1_color)
    yart2.label.set_color(ax2_color)
    yart3.label.set_color(ax3_color)

    figure.set_size_inches(10, 5)
    figure.subplots_adjust(left=0.09, right=0.84)

    return figure, host_ax, par_ax1, par_ax2
