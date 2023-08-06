import pandas as pd

from .common import df_types_and_stats


def df_peek(df: pd.DataFrame, label: str = ''):
    """Take a quick peek at a DF's strucutre, data, and stats.
    """
    print(f"\n--- DF {df.shape} {label}:")
    print("\t> TYPES & STATS:")
    print(df_types_and_stats(df))
    print("\n\t> DATA:")
    with pd.option_context(
        "display.max_rows", 100,
        "display.max_columns", 4,
        'display.width', 200,
    ):
        print(df.T)
