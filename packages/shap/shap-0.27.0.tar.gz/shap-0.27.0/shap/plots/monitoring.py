import numpy as np
import scipy
try:
    import matplotlib.pyplot as pl
    import matplotlib
except ImportError:
    pass
from . import labels
from . import colors


def truncate_text(text, max_len):
    if len(text) > max_len:
        return text[:int(max_len/2)-2] + "..." + text[-int(max_len/2)+1:]
    else:
        return text

def shift_score(x, num_partitions=10):
    """ Return a P-value and index where x has a significant shift in distribution as it goes along.
    """
    inc = int(len(x) / num_partitions)
    if x.std() == 0:
        return 1.0
    pvals = []
    for i in range(inc, len(x)-inc, inc):
        if np.sum(x[:i] != np.median(x[:i])) < 10 or np.sum(x[i:] != np.median(x[i:])) < 10:
            pval = 1.0
        else:
            _,pval = scipy.stats.mannwhitneyu(x[:i], x[i:], alternative="two-sided")
        pvals.append(pval)
    return np.nanmin(pvals), np.argmin(pvals) * inc + inc

def monitoring_plot(ind, shap_values, features=None, feature_names=None, show=True):
    """ Create a SHAP monitoring plot.
    
    (Note this function is preliminary and subject to change!!)
    A SHAP monitoring plot is meant to display the behavior of a model
    over time. Often the shap_values given to this plot explain the loss
    of a model, so changes in a feature's impact on the model's loss over
    time can help in monitoring the model's performance.

    Parameters
    ----------
    ind : int
        Index of the feature to plot.

    shap_values : numpy.array
        Matrix of SHAP values (# samples x # features)

    features : numpy.array or pandas.DataFrame
        Matrix of feature values (# samples x # features)

    feature_names : list
        Names of the features (length # features)
    """
    
    if str(type(features)).endswith("'pandas.core.frame.DataFrame'>"):
        if feature_names is None:
            feature_names = features.columns
        features = features.values
    
    if feature_names is None:
        feature_names = ["Feature " + str(i) for i in range(shap_values.shape[1])]
        
    pl.figure(figsize=(10,3))
    ys = shap_values[:,ind]
    xs = np.arange(len(ys))
    min_pval,min_pval_ind = shift_score(ys)
    
    if min_pval < 0.05 / shap_values.shape[1]:
        pl.axvline(min_pval_ind, linestyle="dashed", color="#666666", alpha=0.2)
    
    if features is None:
        pl.scatter(xs, ys, s=10, cmap=colors.red_blue_solid)
    else:
        pl.scatter(xs, ys, s=10, c=features[:,ind], cmap=colors.red_blue_solid)
        
        cb = pl.colorbar()
        cb.outline.set_visible(False)
        bbox = cb.ax.get_window_extent().transformed(pl.gcf().dpi_scale_trans.inverted())
        cb.ax.set_aspect((bbox.height - 0.7) * 20)
        cb.set_label(truncate_text(feature_names[ind], 30), size=13)
    
    pl.xlabel("Sample index")
    pl.ylabel(truncate_text(feature_names[ind], 30) + "\nSHAP value", size=13)
    pl.gca().xaxis.set_ticks_position('bottom')
    pl.gca().yaxis.set_ticks_position('left')
    pl.gca().spines['right'].set_visible(False)
    pl.gca().spines['top'].set_visible(False)
    
    if show:
        pl.show()