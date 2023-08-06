import pandas as pd


def df_types_and_stats(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum().sort_index()
    missing_pc = (missing / len(df) * 100).round(2)
    types_and_missing = pd.DataFrame(
        {
            'type': df.sort_index().dtypes,
            'missing #': missing,
            'missing %': missing_pc
        },
        index=df.columns.sort_values()
    )
    desc = df.describe(include='all').T.sort_index()
    return pd.concat([types_and_missing, desc], axis=1)
