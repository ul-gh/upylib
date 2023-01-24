from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots_adjust, figure as pyplot_fig
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot

def plot_3_axes(
        ax1_color: str = "red",
        ax2_color: str = "green",
        ax3_color: str = "blue",
        figure = None
        ) -> tuple[Figure, Axes, Axes, Axes]:
    """Plot three individually auto-scaled sets of data on a single X-axis
    
    First Y-axis is located on the left side of the plot,
    second and third Y-axes are placed on the right hand side.
    """
    if figure is None:
        figure = pyplot_fig()
    host_ax = host_subplot(111, axes_class=axisartist.Axes, figure=figure)
    par1 = host_ax.twinx()
    par2 = host_ax.twinx()
    subplots_adjust(right=0.75)
    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)
    
    host_ax.axis["left"].label.set_color(ax1_color)
    par1.axis["right"].label.set_color(ax2_color)
    par2.axis["right"].label.set_color(ax3_color)

    return host_ax.get_figure(), host_ax, par1, par2
