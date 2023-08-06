# -*- coding: utf-8 -*- 

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, FormatStrFormatter

from ..utils.datetime_utils import to_date_object, to_date_str


def plot_kline_to_ax(df, ax=None, bar_width=0.4, color_up='r', color_down='g', alpha=1.0):
    """
    输出K线图到fig
    :param ax: axes
    :param df:
    :param color_down:
    :param color_up:
    :param bar_width:
    :param alpha:
    :return:
    """
    if df is None:
        return

    if ax is None:
        ax = plt.gca()

    xticks = range(0, len(df))  # 需要新的x值, 否则日期中间会有多余空间
    ax.set_xticks(xticks)

    OFFSET = bar_width / 2.0

    t = 0
    for i, q in df.iterrows():
        open, close, high, low = q.open, q.close, q.high, q.low

        if close >= open:
            color = color_up
            lower = open
            height = close - open
        else:
            color = color_down
            lower = close
            height = open - close

        vline = Line2D(
            xdata=(t, t), ydata=(low, high),
            color=color,
            linewidth=1,
            antialiased=True,
        )

        rect = Rectangle(
            xy=(t - OFFSET, lower),
            width=bar_width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        rect.set_alpha(alpha)

        ax.add_line(vline)
        ax.add_patch(rect)

        t += 1

    if df.columns.contains('ma5'):
        prices = df['ma5']
        plt.plot(prices.index, prices.values, color='#000000')
    if df.columns.contains('ma10'):
        prices = df['ma10']
        plt.plot(prices.index, prices.values, color='#9C00F8')
    if df.columns.contains('ma20'):
        prices = df['ma20']
        plt.plot(prices.index, prices.values, color='#FFA600')
    if df.columns.contains('ma30'):
        prices = df['ma30']
        plt.plot(prices.index, prices.values, color='#00008A')

    ax.autoscale_view()


def plot_volume_to_ax(df, ax=None, bar_width=0.4, color_up='r', color_down='g', alpha=1.0):
    """
    输出K线图到fig
    :param ax: axes
    :param df:
    :param color_down:
    :param color_up:
    :param bar_width:
    :param alpha:
    :return:
    """
    if df is None:
        return

    OFFSET = bar_width / 2.0

    t = 0
    for i, q in df.iterrows():
        pt = q['pt']
        volume = q['money']

        if pt > 0:
            color = color_up
        else:
            color = color_down
        height = volume

        # 成交量
        rect = Rectangle(
            xy=(t - OFFSET, 0),
            width=bar_width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        rect.set_alpha(alpha)

        ax.add_patch(rect)

        t += 1


def plot_quote(df, ax=None, figsize=(15, 8), title=None, ylabels=['价格', '成交(万元)']):
    if ax is None:
        fig = plt.figure(figsize=figsize)

    # 两个子图的比例为 3:1
    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
    ax2 = plt.subplot2grid((4, 1), (3, 0), sharex=ax1)  # 共用一个x坐标轴
    fig.subplots_adjust(hspace=0)  # 两个子图之间的距离

    plt.sca(ax1)  # 选择子图1
    ax = ax1

    if title is not None:
        plt.title(title);
    if ylabels is not None:
        plt.ylabel(ylabels[0])
    plot_kline_to_ax(df, ax)

    # ax.grid(True, axis='y')
    ax.yaxis.tick_right()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.tick_params(axis="y", direction='in', pad=0)
    ax.tick_params(axis="x", direction='in', pad=0, labelrotation=0)

    if df is not None and len(df) > 0:
        ymin = df['low'].min()
        ymax = df['high'].max()
        ax.set_yticks([ymin, df['close'].mean(), ymax])
        ax.set_ylim(ymin - (ymax - ymin) * .05, ymax)

    plt.setp(ax.xaxis.get_majorticklabels(), visible=False)  # 隐藏 x 轴标签

    if df is not None and len(df) > 0:
        def fmt_date_weekday(x, pos):
            dt = to_date_object(df.index[x])
            wd = dt.weekday()
            return to_date_str(dt)[-5:] + '(周' + '一二三四五六日'[wd] + ')'

        ax.xaxis.set_major_formatter(FuncFormatter(fmt_date_weekday))

        xticks = []
        for x in ax.get_xticks():
            dt = to_date_object(df.index[x])
            wd = dt.weekday()
            if wd == 0:
                xticks.append(x)
        ax.set_xticks(xticks)
    ax.autoscale_view()

    plt.sca(ax2)  # 选择子图2
    ax = ax2

    if ylabels is not None:
        plt.ylabel(ylabels[1])
    plot_volume_to_ax(df, ax)

    ax.grid(True)
    ax.yaxis.tick_right()
    ax.tick_params(axis="y", direction='in', pad=0)
    if df is not None and len(df) > 0:
        ymax = round(df['money'].max())
        ylast = round(df['money'][-1])
        ymean = round(df['money'].mean())
        ax.set_yticks([ymean, ylast, ymax])
        ax.set_ylim(0, ymax)
    ax.autoscale_view()

    return ax1, ax2


def plot_index(df, ax=None, figsize=(15, 8), title=None, ylabels=['指数', '成交(亿元)']):
    return plot_quote(df, ax, figsize, title, ylabels)
