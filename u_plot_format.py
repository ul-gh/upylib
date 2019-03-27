# -*- coding: utf-8 -*-
import matplotlib.ticker as ticker
# pip install mpldatacursor
from mpldatacursor import datacursor


class EngLogFormatter(ticker.LogFormatter):
    """Re-Format output of LogFormatter instance call with engineering number
    format and SI prefixes"""
    format_eng = ticker.EngFormatter(places=1, unit=" ", sep="\N{THIN SPACE}")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        str = super().__call__(*args, **kwargs)
        if str:
            return self.format_eng(float(str))
        else:
            return ""


def axes_log_log_engineering(ax):
    """Set x and y axis to logarithmic scale base 10 with engineering number
    format and SI prefixes
    """
    # Define axis labels format
    format_eng = ticker.EngFormatter(places=1, unit=" ", sep="\N{THIN SPACE}")
    # ticks_log_E6 = ticker.LogLocator(subs=(1.0, 1.5, 2.2, 3.3, 4.7, 6.8))
    # equivalent: plt.ylabel(), plt.ylim(), plt.yscale() usw.
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.tick_params(axis="both", which="major", length=6.0)
    # x-axis ticks and labels
    ax.xaxis.set_major_formatter(format_eng)
    ax.xaxis.set_minor_formatter(EngLogFormatter(minor_thresholds=(2, 0.5)))
    # y-axis ticks and labels
    ax.yaxis.set_major_formatter(format_eng)
    ax.yaxis.set_minor_formatter(EngLogFormatter(minor_thresholds=(2, 0.5)))
    ax.yaxis.set_major_locator(ticker.LogLocator())


def axes_log_lin_engineering(ax):
    """Set x axis to logarithmic scale base 10 and y axis to linear scale
    with engineering number format and SI prefixes
    """
    # Define axis labels format
    format_eng = ticker.EngFormatter(places=1, unit=" ", sep="\N{THIN SPACE}")
    # ticks_log_E6 = ticker.LogLocator(subs=(1.0, 1.5, 2.2, 3.3, 4.7, 6.8))
    # equivalent: plt.ylabel(), plt.ylim(), plt.yscale() usw.
    ax.set_yscale("linear")
    ax.set_xscale("log")
    ax.tick_params(axis="both", which="major", length=6.0)
    # x-axis ticks and labels
    ax.xaxis.set_major_formatter(format_eng)
    ax.xaxis.set_minor_formatter(EngLogFormatter(minor_thresholds=(2, 0.5)))
    # y-axis ticks and labels
    ax.yaxis.set_major_formatter(format_eng)
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())


def add_datacursor_engineering(plot_lines):
    """Add cursor with engineering number format and SI unit prefixes to the
    plot lines list object
    """
    # Define axis ticks and labels format
    format_eng = ticker.EngFormatter(places=1, unit=" ", sep="\N{THIN SPACE}")
    def eng_xy(**kwargs):
        # Formats x and y kwargs as two-line string with engineering notation
        xf = format_eng(kwargs["x"])
        yf = format_eng(kwargs["y"])
        return "{}\n{}".format(xf, yf)
    #datacursor(pl_1, formatter="{x:3.1f}\n{y:1.3e}".format)
    datacursor(plot_lines, formatter=eng_xy)


def plot_engineering(
        ax,
        *args,
        title="Title",
        xlabel="X-Axis Label",
        ylabel="Y-Axis Label",
        xlim=(None, None),
        ylim=(None, None),
        **kwargs
        ):
    plot_lines = ax.plot(*args, **kwargs)
    add_datacursor_engineering(plot_lines)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def plot_log_log_engineering(ax, *args, **kwargs):
    axes_log_log_engineering(ax)
    plot_engineering(ax, *args, **kwargs)


def plot_log_lin_engineering(ax, *args, **kwargs):
    axes_log_lin_engineering(ax)
    plot_engineering(ax, *args, **kwargs)