import numpy as np

from mjtracker.interface_mj import apply_mj
from pandas import DataFrame


# Function to compute rank based on the number of medals
def rank_by_total_medals(df) -> DataFrame:
    df['Rank_Total'] = df['Total'].rank(method='min', ascending=False).astype(int)
    return df.sort_values(by='Rank_Total')


# Function to compute rank based on lexicographic order (gold > silver > bronze)
def rank_lexicographically(df) -> DataFrame:
    df = df.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False)
    df["Rank_Lexico"] = np.linspace(1, len(df), len(df), dtype=int)
    return df.sort_values(by='Rank_Lexico')


def apply_majority_judgment(df_mj) -> DataFrame:
    return apply_mj(df_mj, rolling_mj=False, official_lib=True, reversed=True)