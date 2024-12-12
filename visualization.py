# visualization.py

import plotly.express as px
import pandas as pd

def create_bar_chart(df: pd.DataFrame, x_column: str, y_column: str, title: str, xaxis_title: str, yaxis_title: str):
    """Create a bar chart for the given DataFrame."""
    fig = px.bar(df, x=x_column, y=y_column, 
                 title=title, labels={x_column: xaxis_title, y_column: yaxis_title})

    # Set the x-axis labels to be rotated for better visibility (optional)
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(tickangle=45)  # Rotate the x-axis labels by 45 degrees to prevent overlap
    )

    fig.update_traces(text=df[x_column], hoverinfo="text")  # Show usernames on hover
    return fig
