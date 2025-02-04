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
        path=[px.Constant("all"), "industry", "full_name"],  # variables outside -> inside
        values="net_worth",  # count based on net worth
        color='industry',  # color based on industry
        color_continuous_scale="turbo",
        maxdepth=3
    )

    # Update layout
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=30),
    )
    
    return fig

if __name__ == "__main__":
    print("This module is not meant to be run directly")
