from matplotlib.pyplot import subplots_adjust
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot

def plot_3_traces(
        x_data,
        y1_data,
        y2_data,
        y3_data,
        x_label: str = "",
        y1_label: str = "",
        y2_label: str = "",
        y3_label: str = "",
        y1_format: str = "r-",
        y2_format: str = "g-",
        y3_format: str = "b-",
        figure = None
        ):
    """Plot three individually auto-scaled sets of data on a single X-axis
    
    First Y-axis is located on the left side of the plot,
    second and third Y-axes are placed on the right hand side.
    """
    host_ax = host_subplot(111, axes_class=axisartist.Axes, figure=figure)
    par1 = host_ax.twinx()
    par2 = host_ax.twinx()
    subplots_adjust(right=0.75)
    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)

    traces1 = host_ax.plot(x_data, y1_data, y1_format, label=y1_label)
    traces2 = par1.plot(x_data, y2_data, y2_format, label=y2_label)
    traces3 = par2.plot(x_data, y3_data, y3_format, label=y3_label)

    host_ax.legend()

    host_ax.axis["left"].label.set_color(traces1[0].get_color())
    par1.axis["right"].label.set_color(traces2[0].get_color())
    par2.axis["right"].label.set_color(traces3[0].get_color())

    host_ax.set_xlabel(x_label)
    host_ax.set_ylabel(y1_label)
    par1.set_ylabel(y2_label)
    par2.set_ylabel(y3_label)

    return host_ax.get_figure(), traces1, traces2, traces3