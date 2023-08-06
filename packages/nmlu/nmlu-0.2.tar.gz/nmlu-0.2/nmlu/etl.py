import pandas as pd
from sklearn.utils import shuffle
from typing import List, Sequence, Tuple


def convert_cats(df: pd.DataFrame, extra_cats={}):
    """Convert string values and what we know are categories to categorical vars.

    Parameters
    ----------
    df
    extra_cats : sequence or set of str
        Extra column names that we want to turn to categories regardless of their actual type.
    """
    for n, c in df.items():
        if pd.api.types.is_string_dtype(c) or n in extra_cats:
            df[n] = c.astype('category').cat.as_ordered()


def fill_missing(df: pd.DataFrame, how):
    """Fill missing data for numeric columns.
    """
    assert how in {'median'}
    for col_name, col in df.items():
        if pd.api.types.is_numeric_dtype(col):
            if pd.isnull(col).sum():
                if how == 'median':
                    df[col_name] = col.fillna(col.median())


def numericalize(df: pd.DataFrame, nans_to_zero=True):
    """Numericalize categories (and optionally get rid of -1's for NaNs)"""
    for n, c in df.items():
        if not pd.api.types.is_numeric_dtype(c):
            df[n] = df[n].cat.codes + 1
            if nans_to_zero:  # NaN's become -1, so we add 1 to make them 0
                df[n] += 1


def train_test_xy_split(
    df: pd.DataFrame,
    y_cols: Sequence[str],
    train_sz: int = 0,
    train_fr: float = 0.0,
    shuffle: bool = False,
    random_sate: int = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Train/test and x/y splitting of df (optionally shuffle).

    Returns
    -------
    x_train
    x_test
    y_train
    y_test
    """
    assert train_sz or train_fr
    assert not (train_sz and train_fr)
    if train_fr:  # either five train_sz *or* train_fr, not both
        assert train_fr > 0 and train_fr <= 1

    if shuffle:  # NOTE: sklear.utils.shuffle MAY be faster for some data
        df = df.sample(frac=1, random_sate=random_sate)

    y = df[y_cols]
    x = df.drop(y_cols, axis=1)

    if not train_sz:
        train_sz = int(len(df) * train_fr)

    x_train = x.iloc[:train_sz]
    y_train = y.iloc[:train_sz]
    x_test = x.iloc[train_sz:]
    y_test = y.iloc[train_sz:]

    if len(y_cols) == 1:
        y_train = y_train.values[:, 0]
        y_test = y_test.values[:, 0]

    return x_train, x_test, y_train, y_test
