"""
Industry treemap visualization for the Billionaires Dashboard.
"""
import plotly.express as px

def create_treemap(year_df):
    """Create the industry treemap visualization."""
    # Filter out rows with missing industry
    filtered_df = year_df.dropna(subset=['industry'])

    # Create treemap
    fig = px.treemap(
        filtered_df,
        path=[px.Constant("Total"), "industry", "full_name"],  # variables outside -> inside
        values="net_worth",  # count based on net worth
        color='industry',  # color based on industry
        color_discrete_sequence=px.colors.sequential.Agsunset,
        maxdepth=3)

    fig.update_traces(
        textinfo="label+value",  # Show name and net worth inside the boxes
        texttemplate="%{label}<br>Net Worth: $%{value:.2f}B",
        hovertemplate="<b>%{label}</b><br>Net Worth: $%{value:.2f}B",
    )

    fig.update_layout(
        height=370,
        margin=dict(l=0, r=0, t=0, b=0),  # Minimal margins
    )

    return fig

if __name__ == "__main__":
    print("This module is not meant to be run directly")
