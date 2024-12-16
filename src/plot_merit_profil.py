from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express as px


def plot_merit_profiles_in_number(
    df: DataFrame,
    grades: list,
    auto_text: bool = True,
    font_size: int = 20,
    date: str = None,
    sponsor: str = None,
    source: str = None,
    show_no_opinion: bool = True,
) -> go.Figure:
    df = df.copy()

    nb_grades = len(grades)

    # compute the list sorted of candidat names to order y axis.
    candidat_list = list(df["candidat"])
    rank_list = list(df["rang"] - 1)
    sorted_candidat_list = [i[1] for i in sorted(zip(rank_list, candidat_list))]
    r_sorted_candidat_list = sorted_candidat_list.copy()
    r_sorted_candidat_list.reverse()

    # colors = color_palette(palette="coolwarm", n_colors=nb_grades)
    # Gold, Silver, Bronze, No Medal
    colors_olympics = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (139, 69, 19)]
    colors = colors_olympics
    color_dict = {f"intention_mention_{i + 1}": f"rgb{str(colors[i])}" for i in range(nb_grades)}
    fig = px.bar(
        df,
        x=get_intentions_colheaders(df, nb_grades),
        y="candidat",
        orientation="h",
        text_auto=auto_text,
        color_discrete_map=color_dict,
    )

    fig.update_traces(textfont_size=font_size, textangle=0, textposition="auto", cliponaxis=False, width=0.5)

    # replace variable names with grades
    new_names = {f"intention_mention_{i + 1}": grades[i] for i in range(nb_grades)}
    fig.for_each_trace(
        lambda t: t.update(
            name=new_names[t.name],
            legendgroup=new_names[t.name],
            hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name]),
        )
    )

    # vertical line
    sum_of_intentions = df[get_intentions_colheaders(df, nb_grades)].sum(axis=1).max()
    fig.add_vline(x=sum_of_intentions/2, line_width=2, line_color="black")

    # Legend
    fig.update_layout(
        legend_title_text=None,
        autosize=True,
        legend=dict(orientation="h", xanchor="center", x=0.5, y=-0.05),  # 50 % of the figure width
    )

    fig.update(data=[{"hovertemplate": "Intention: %{x}<br>Candidat: %{y}"}])
    # todo: need to plot grades in hovertemplate.

    # no background
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    # xticks and y ticks
    # Add sans opinion to y tick label # todo : it may be simplified !
    if show_no_opinion and not np.isnan(df["sans_opinion"].unique()[0]):
        df["candidat_sans_opinion"] = None
        for ii, cell in enumerate(df["candidat"]):
            df["candidat_sans_opinion"].iat[ii] = (
                "<b>" + cell + "</b>" + "     <br><i>(sans opinion " + str(df["sans_opinion"].iloc[ii]) + "%)</i>     "
            )
        # compute the list sorted of candidat names to order y axis.
        candidat_list = list(df["candidat_sans_opinion"])
        rank_list = list(df["rang"] - 1)
        sorted_candidat_list = [i[1] for i in sorted(zip(rank_list, candidat_list))]
        r_sorted_candidat_no_opinion_list = sorted_candidat_list.copy()
        r_sorted_candidat_no_opinion_list.reverse()
        yticktext = r_sorted_candidat_no_opinion_list
    else:
        yticktext = ["<b>" + s + "</b>" + "     " for s in r_sorted_candidat_list]

    # xticks and y ticks
    fig.update_layout(
        xaxis=dict(
            title="",  # intentions
        ),
        yaxis=dict(
            tickfont_size=font_size * 0.75,
            title="",  # candidat
            automargin=True,
            ticklabelposition="outside left",
            ticksuffix="   ",
            tickmode="array",
            tickvals=[i for i in range(len(df))],
            ticktext=yticktext,
            categoryorder="array",
            categoryarray=r_sorted_candidat_list,
        ),  # space
    )

    # Title and detailed

    date_str = f"date: {date}, " if date is not None else ""
    source_str = f"source: {source}" if source is not None else ""
    source_str += ", " if sponsor is not None else ""
    sponsor_str = f"commanditaire: {sponsor}" if sponsor is not None else ""
    title = "<b>Ranking with Majority Judgement</b> <br>" + f"<i>{date_str}{source_str}{sponsor_str}</i>"
    fig.update_layout(title=title, title_x=0.5)

    # font family
    fig.update_layout(font_family="arial")

    fig = _add_image_to_fig(fig, x=0.9, y=1.01, sizex=0.15, sizey=0.15)

    # size of the figure
    fig.update_layout(width=1000, height=600)

    return fig


def _add_image_to_fig(
    fig: go.Figure, x: float, y: float, sizex: float, sizey: float, xanchor: str = "left"
) -> go.Figure:
    """
    Add mieux voter logo to the figure

    Parameters
    ----------
    fig : go.Figure
       figure to add the date to
    x : float
        x position of the logo
    y : float
        y position of the logo
    sizex : float
        x size of the logo
    sizey : float
        y size of the logo
    xanchor : str
        x anchor of the logo (left, center, right)
    Returns
    -------
    The figure with the logo
    """
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/MieuxVoter/majority-judgment-tracker/main/icons/logo.svg",
            xref="paper",
            yref="paper",
            x=x,
            y=y,
            sizex=sizex,
            sizey=sizey,
            xanchor=xanchor,
            yanchor="bottom",
        )
    )
    return fig


def get_intentions_colheaders(df: DataFrame, nb_mentions: int = 7):
    """
    Get the colheaders of the intentions of votes

    Parameters
    ----------
    df : DataFrame
       DataFrame containing the surveys
    nb_mentions : int
       Number of mentions
    Returns
    -------
       List of colheaders of the intentions of votes
    """
    list_col = df.columns.to_list()
    intentions_colheader = [s for s in list_col if "intention" in s]
    return intentions_colheader[:nb_mentions]


def get_grades(df: DataFrame, nb_mentions: int = 7) -> list:
    """
    Get the grades of the candidates

    Parameters
    ----------
    df : DataFrame
       DataFrame containing the surveys
    nb_mentions : int
       Number of mentions
    Returns
    -------
       List of grades of the candidates
    """
    list_col = df.columns.to_list()
    mentions_colheader = [s for s in list_col if "mention" in s and not "intention" in s and not "nombre" in s]
    mentions_colheader = mentions_colheader[:nb_mentions]
    numpy_mention = df[mentions_colheader].to_numpy().tolist()[0]

    numpy_mention = [m for m in numpy_mention if m != "nan"]
    return numpy_mention
