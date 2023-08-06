import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def pairs_dists_plot(df, y_col=None, except_cols=None, figsize=None):
    if except_cols is None:
        except_cols = set()
    if y_col is not None:
        except_cols.add(y_col)
    return sns.pairplot(
        df,
        hue=y_col,
        vars=set(df.columns.values).difference(except_cols),
    )


def heatmap_plot(df, figsize=(16, 16)):
    fig, ax = plt.subplots(figsize=figsize)
    return sns.heatmap(df.corr(), annot=True, ax=ax)


def pairs_corr_plot(df, figsize=(18, 16)):
    axes = pd.plotting.scatter_matrix(df, alpha=0.3, figsize=figsize, diagonal='kde')
    corr = df.corr().values
    for i, j in zip(*np.triu_indices_from(axes, k=1)):
        axes[i, j].annotate("%.3f" % corr[i, j], (0.8, 0.8), xycoords='axes fraction', ha='center', va='center')
