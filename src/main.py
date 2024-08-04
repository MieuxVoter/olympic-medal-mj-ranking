import os
import numpy as np
import pandas as pd
import plotly.express as px

from plot_merit_profil import plot_merit_profiles_in_number, get_grades
from ranking_functions import apply_majority_judgment, rank_lexicographically, rank_by_total_medals
from scraper import scrap_olympic_data
from table_function import create_ranking_comparison_table

# Constants
GOLD_MEDAL = "\U0001F947"
SILVER_MEDAL = "\U0001F948"
BRONZE_MEDAL = "\U0001F949"
CHOCOLATE = "\U0001F36B"
PATH = os.path.dirname(os.path.abspath(__file__)) + '/../data'
OUTPATH = os.path.dirname(os.path.abspath(__file__)) + '/../figures'


def load_data():
    df, suffix = scrap_olympic_data()
    fin_enquete = f"{suffix[:4]}-{suffix[4:6]}-{suffix[6:8]} {suffix[9:11]}:00"
    return df, fin_enquete


def verify_medal_sum(df):
    return (df["Gold"] + df["Silver"] + df["Bronze"] == df["Total"]).all()


def filter_countries(df, min_medals):
    return df[df["Total"] >= min_medals]


def create_mj_dataframe(df, fin_enquete):
    df_mj = pd.DataFrame()
    df_mj["candidat"] = df["Country"]
    df_mj["nombre_mentions"] = 4

    mentions = [
        ("Gold", GOLD_MEDAL),
        ("Silver", SILVER_MEDAL),
        ("Bronze", BRONZE_MEDAL),
        ("No Medal", CHOCOLATE)
    ]

    for i, (mention, emoji) in enumerate(mentions, 1):
        df_mj[f"mention_{i}"] = f"{mention} {emoji}"
        df_mj[f"intention_mention_{i}"] = df[mention] if mention != "No Medal" else df["Total"].max() - df["Total"]

    for i in range(5, 8):
        df_mj[f"mention_{i}"] = np.nan
        df_mj[f"intention_mention_{i}"] = np.nan

    df_mj["nom_institut"] = "Olympics 2024"
    df_mj["commanditaire"] = "Mieux Voter"
    df_mj["debut_enquete"] = np.nan
    df_mj["fin_enquete"] = fin_enquete
    df_mj["id"] = 1

    return df_mj


def get_plot_info(df_mj_ranked):
    first_idx = df_mj_ranked.first_valid_index()
    source = df_mj_ranked["nom_institut"].loc[first_idx]
    date = df_mj_ranked["fin_enquete"].loc[first_idx]
    nb_grades = df_mj_ranked["nombre_mentions"].unique()[0]
    grades = get_grades(df_mj_ranked, nb_grades)
    return source, date, grades


def plot_merit_profiles(df_mj_ranked, source, date, grades):
    fig = plot_merit_profiles_in_number(
        df=df_mj_ranked,
        grades=grades,
        auto_text=True,
        source=source,
        date=date,
        sponsor=None,
        show_no_opinion=False,
    )
    return fig


def save_plot(fig, filename):
    fig.write_image(filename, format='pdf')


def main():
    df, fin_enquete = load_data()

    if not verify_medal_sum(df):
        print("Warning: Medal sum verification failed")

    MIN_MEDALS = 5

    df = filter_countries(df, MIN_MEDALS)
    df_mj = create_mj_dataframe(df, fin_enquete)
    df_mj_ranked = apply_majority_judgment(df_mj)

    source, date, grades = get_plot_info(df_mj_ranked)

    # fake plot to hack an artefact that disappear when done before the main one.
    fig1 = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    fig1.show()

    fig = plot_merit_profiles(df_mj_ranked, source, date, grades)
    fig.show()

    save_plot(fig, f"{OUTPATH}/mj_olympic_{fin_enquete}.pdf")
    fig.write_image(f"{OUTPATH}/mj_olympic_{fin_enquete}.png", format='png')

    df, _ = load_data()
    df_mj = create_mj_dataframe(df, fin_enquete)
    df_mj_ranked = apply_majority_judgment(df_mj)
    df = rank_lexicographically(df)
    df = rank_by_total_medals(df)

    df_mj_ranked["rang"] = df_mj_ranked["rang"].apply(lambda x: x + 1)

    rank_comparison = pd.merge(
        left=df_mj_ranked[["candidat", "rang", "mention_majoritaire"]],
        right=df[["Country", "Rank_Total", "Rank_Lexico", "Total", "Gold", "Silver", "Bronze"]],
        left_on="candidat",
        right_on="Country",
    )

    rank_comparison["Rank_MJ"] = rank_comparison["rang"]
    rank_comparison = rank_comparison.drop(columns=["rang", "candidat"])

    fig = create_ranking_comparison_table(rank_comparison)
    fig.write_image(f"{OUTPATH}/mj_olympic_table_{fin_enquete}.png", format='png')
    save_plot(fig, f"{OUTPATH}/mj_olympic_table_{fin_enquete}.pdf")
    fig.show()


if __name__ == "__main__":
    main()
