import numpy as np
import pandas as pd
import seaborn as sns
import  matplotlib.pyplot as plt
from pathconf import plots_path


def make_meshgrid(x, y, h = .02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy

def predict(ndsvm, node, mesh):
    alpha, beta, b = ndsvm.get_best_local_classifier(node)

    p = []
    for i in range(mesh.shape[0]):
        p.append(ndsvm.local_discriminant(node, alpha, beta, b, mesh[i]))

    return np.array(p)

def plot_contours_scatter(model, node, xx, yy, X, y, name, dist, **params):
    plt.figure()

    if dist:
        z = predict(model, node, np.c_[xx.ravel(), yy.ravel()])
    else:
        z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)
    plt.contourf(xx, yy, z, **params)
    plt.scatter(X[:, 0], X[:, 1], c = y, cmap = plt.cm.coolwarm, s=20, edgecolors='k')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    file = str(plots_path) + "/" + name + ".pdf"
    plt.savefig(file, transparent = True)


def plot_non_linear_classifier(model, X, y, name, node = 0, dist = True):
    sns.set_style('ticks')

    xx, yy = make_meshgrid(X[:, 0], X[:, 1])

    plot_contours_scatter(model, node, xx, yy, X, y, name, dist, cmap = plt.cm.coolwarm, alpha=0.82)

