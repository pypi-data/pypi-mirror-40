# bar_chart.py
# Author: Joshua Beard
# Created: 2019-01-08
import numpy as np
from matplotlib import pyplot as plt


def plot_separate(data,
                  labels=None,
                  bar_width=0.75,
                  figsize=(12, 8),
                  title='',
                  ylim=None,
                  max_val_pad=None,
                  sort_order=None,
                  use_bottom_labels=False,
                  use_legend=False,
                  show_max_val=False,
                  show=True,
                  save=False,
                  save_name=None,
                  scale_by=None,
                  label_bars=None,
                  label_bars_format='percent',
                  ):

    string_dtype = np.dtype('<U1')

    data = np.array(data)
    labels = np.array(labels)

    if sort_order is not None:
        order = np.argsort(data)
        if sort_order.lower() == 'descending':
            order = order[::-1]

        data = np.array(data)[order]
        labels = labels[order]

    n_total = data.sum()

    if use_bottom_labels and labels is not None:
        bottom_labels = [labels[i] + '\nN = {}'.format(data[i])
                         for i in range(len(labels))]
        if len(labels) > 6:
            # TODO test this
            label_rotation = 45
        else:
            label_rotation = 0
    else:
        bottom_labels = None

    if scale_by is not None:
        data = data / scale_by
        n_total = 1

    # Separation between bars
    # TODO different logic if labels are numbers?
    if labels.dtype == string_dtype:
        offsets = list(range(len(labels)))
    else:
        offsets = list(range(len(labels)))

    # Now it's time to actually plot the thing
    bars = []
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    for i in range(len(labels)):
        bars.append(ax.bar(offsets[i], data[i], bar_width))

    if show_max_val:
        ax.plot([min(offsets) - 1, max(offsets) + 1],
                [n_total, n_total],
                '--',
                color=[0.75, 0.75, 0.75])

    if label_bars is not None:

        if label_bars_format.lower() == 'percent':
            def fmt(x):
                return '{:.1f}%'.format(x * 100)
        else:
            def fmt(x):
                return '{}'.format(x)

        if label_bars.lower() == 'above':
            if scale_by is not None:
                y_offset = 0.05

        for i in range(len(labels)):
            plt.text(x=offsets[i], y=data[i] + y_offset, s=fmt(data[i]))

    if ylim is None:
        if max_val_pad is None:
            max_val_pad = .1

        ylim = (0, max(data) + max(data) * max_val_pad)

    ax.set_ylim(ylim)
    ax.set_xlim(-bar_width, (len(data) - 1) + bar_width)
    ax.set_xticks(offsets)

    if bottom_labels is not None:
        xtick_labels = ax.set_xticklabels(bottom_labels)
        plt.setp(xtick_labels, rotation=label_rotation)

    if use_legend:
        ax.legend(bars, labels, prop={'size': max(figsize)})

    fig.suptitle(title, fontsize=max(figsize) * 2)
    plt.tick_params(labelsize=max(figsize))

    if save:
        if save_name is not None:
            plt.savefig(save_name)
        else:
            plt.savefig(title)

    if show:
        plt.show()
