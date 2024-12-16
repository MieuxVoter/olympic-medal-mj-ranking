import pandas as pd
import plotly.graph_objects as go

# Sample data
data = {
    "Flag": [
        "🇨🇳", "🇫🇷", "🇦🇺", "🇺🇸", "🇬🇧",
        "🇰🇷", "🇯🇵", "🇮🇹"
    ],
    "NOC": ["People's Republic of China", "France", "Australia", "United States of America", "Great Britain",
            "Republic of Korea", "Japan", "Italy"],
    "Gold": [16, 12, 12, 11, 10, 9, 8, 6],
    "Silver": [11, 14, 7, 20, 10, 6, 5, 8],
    "Bronze": [9, 15, 5, 20, 12, 5, 9, 4],
    "Total": [36, 41, 24, 51, 32, 20, 22, 18]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Sorting the data
df = df.sort_values(by="Total", ascending=False)

# Define colors
header_color = '#1f77b4'
row_even_color = '#f2f2f2'
row_odd_color = 'white'

# Medal emojis
gold_medal = "\U0001F947"
silver_medal = "\U0001F948"
bronze_medal = "\U0001F949"

# Create a Plotly table with enhanced formatting
fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4,5,6,7],
    columnwidth = [40,40,200,80,80,80,80],
    header=dict(values=["<b>Rank</b>", "<b>Flag</b>", "<b>NOCs</b>", f"<b>{gold_medal} Gold</b>", f"<b>{silver_medal} Silver</b>", f"<b>{bronze_medal} Bronze</b>", "<b>Total</b>"],
                fill_color=header_color,
                align='center',
                font=dict(color='white', size=12),
                height=40),
    cells=dict(values=[list(range(1, len(df)+1)), df.Flag, df.NOC, df.Gold, df.Silver, df.Bronze, df.Total],
               fill_color = [[row_odd_color,row_even_color]*4],
               align = ['center', 'center', 'left', 'center', 'center', 'center', 'center'],
               font = dict(color = 'black', size = 12),
               height = 30),
    )
])

fig.update_layout(
    title_text='Olympic Medal Ranking',
    title_font_size=22,
    title_x=0.5,
    margin=dict(l=20, r=20, t=60, b=20),
    height=600,
    paper_bgcolor='white'
)

fig.show()
