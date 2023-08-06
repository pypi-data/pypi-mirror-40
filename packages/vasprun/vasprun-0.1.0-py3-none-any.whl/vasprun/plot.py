"""
Routines for plotting band-structure and density of states.
"""
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 18,})
matplotlib.rcParams.update({'savefig.dpi': 300, 'savefig.bbox': 'tight',
                            'savefig.pad_inches':0.02,
                            'savefig.transparent':True})

FIGFILEEXT = '.pdf'

GREEK = {'G': r'\Gamma', 'Gamma':  r'\Gamma'}

def plot_bands(data, x_values=None, x_ticks=None, x_tick_labels=None,
               e_fermi=None, e_ref=0, outprefix='',
               figsize=(7, 9), xlim=None, ylim=None,
               xlabel=None, ylabel='Energy (eV)'):
    """Plot band-structure"""
    fig, ax = plt.subplots(figsize=figsize)
    #ax.set_xlabel(r'k (1/$\rm\AA$)')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    #
    if ylim is not None:
        ax.set_ylim(ylim)
    if xlim is None:
        ax.set_xlim(np.min(x_values), np.max(x_values))
    else:
        ax.set_xlim(xlim)
    ax.set_xticks(x_ticks)
    # The following will fail if x_tick_labels has e.g. 'G|X'
    # and requires string handling rather than simple character map
    ax.set_xticklabels([r"$\mathrm{{{}}}$".format(GREEK.get(ch, ch))
                        for ch in x_tick_labels])
    for tick in x_ticks:
        ax.axvline(tick, color='k', lw=1)
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if isinstance(data, list):
        lines = []
        for i in range(len(data)):
            _y = data[i]-e_ref
            if isinstance(x_values, list):
                _x = x_values[i]
            else:
                _x = x_values
            lines.append(ax.plot(_x, _y, color=cycle[i]))
    else:
        y_values = data-e_ref
        lines=ax.plot(x_values, y_values, color='C0')
    if e_fermi is not None:
        ax.axhline(e_fermi-e_ref, color='r', lw=1, ls='--')
    if outprefix:
        fig.savefig(outprefix+'.pdf')
    return fig, ax
