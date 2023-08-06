import matplotlib.pyplot as plt
import numpy as np


from mpl_toolkits import axes_grid1


def _add_colorbar(img, aspect=1.0/20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(img.axes)
    width = axes_grid1.axes_size.AxesY(img.axes, aspect=aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return img.axes.figure.colorbar(img, cax=cax, **kwargs)


def plot_confusion_matrix(cnf_matrix, classes,
                          normalize=True,
                          title='Confusion matrix',
                          ylabel='True class',
                          xlabel='Predicted class',
                          cmap='Blues',
                          colorbar=True,
                          colorbar_aspect_ratio=None,
                          classes_per_inch=5,
                          **kwargs):
    """
    Plot a confusion matrix.
    Normalization can be applied by setting `normalize=True`.

    `kwargs` are parsed on to the `plt.imshow` function.

    Source: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    """
    if normalize:
        normalization_factors = cnf_matrix.sum(axis=1)[:, np.newaxis]
        normalization_factors[normalization_factors == 0] = 1
        cnf_matrix = cnf_matrix.astype('float') / normalization_factors
    fig = plt.gcf()
    width_inches = len(classes) / float(classes_per_inch)
    fig.set_size_inches(width_inches, width_inches)
    img = plt.imshow(cnf_matrix, interpolation='nearest', cmap=cmap, **kwargs)
    plt.title(title)
    if colorbar:
        if colorbar_aspect_ratio is None:
            colorbar_aspect_ratio = max(0.03, 1. / len(classes))
        _add_colorbar(img, aspect=colorbar_aspect_ratio)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.tight_layout()
