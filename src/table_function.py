import plotly.graph_objects as go

GOLD_MEDAL = "\U0001F947"
SILVER_MEDAL = "\U0001F948"
BRONZE_MEDAL = "\U0001F949"
CHOCOLATE = "\U0001F36B"


def create_ranking_comparison_table(rank_comparison):
    # Create three separate dataframes for each ranking method
    df_lexico = rank_comparison[['Country', 'Rank_Lexico', 'Gold', 'Silver', 'Bronze']].sort_values('Rank_Lexico')
    df_total = rank_comparison[['Country', 'Rank_Total', 'Total']].sort_values('Rank_Total')
    df_mj = rank_comparison[['Country', 'Rank_MJ', 'mention_majoritaire']].sort_values('Rank_MJ')

    countries_lexico = (
            df_lexico["Country"].values + "      "
            + df_lexico["Gold"].apply(lambda x: str(x)) + " "
            + GOLD_MEDAL + " "
            + df_lexico["Silver"].apply(lambda x: str(x)) + " "
            + SILVER_MEDAL + " "
            + df_lexico["Gold"].apply(lambda x: str(x)) + " "
            + BRONZE_MEDAL + " "
    )

    countries_total = (
            df_total["Country"].values + "      "
            + df_total["Total"].apply(lambda x: str(x)) + " "
            + GOLD_MEDAL + SILVER_MEDAL + BRONZE_MEDAL
    )
    countries_mj = (
            df_mj["Country"].values + "      "
            + df_mj["mention_majoritaire"].apply(lambda x: str(x))
    )

    # Define colors
    header_color = '#1f77b4'
    row_even_color = '#f2f2f2'
    row_odd_color = 'white'

    # Create a Plotly table with enhanced formatting
    fig = go.Figure(data=[go.Table(
        columnwidth=[40, 160, 160, 160],
        header=dict(values=[
            "<b>Rank</b>",
            f"<b>Lexicographic<br>{GOLD_MEDAL}>{SILVER_MEDAL}>{BRONZE_MEDAL}</b>",
            "<b>Majority Judgment</b>",
            f"<b>Total Medals<br>{GOLD_MEDAL}+{SILVER_MEDAL}+{BRONZE_MEDAL}</b>",
        ],
                    fill_color=header_color,
                    align='center',
                    font=dict(color='white', size=12),
                    height=40),
        cells=dict(values=[
            [i for i in range(1, len(rank_comparison) + 1)],
            countries_lexico,
            countries_mj,
            countries_total,
            ],
                   fill_color=[[row_odd_color, row_even_color]*4],
                   align=['center', 'center', 'center', 'center'],
                   font=dict(color='black', size=12),
                   height=30),
    )])

    fig.update_layout(
        title_text='Comparison of Olympic Ranking Systems',
        title_font_size=22,
        title_x=0.5,
        # margin=dict(l=20, r=20, t=60, b=20),
        # height=max(600, 100 + 30 * max_rows),  # Adjust height based on number of rows
        paper_bgcolor='white'
    )

    return fig
