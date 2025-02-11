"""
Wealth chart visualization for the Billionaires Dashboard.
"""
import plotly.graph_objects as go
from modules.data import get_flag_emoji
from modules.config import PLOT_BGCOLOR, PAPER_BGCOLOR

def create_wealth_chart(year_df):
    """Create the top 20 billionaires bar chart."""
    # Get top 20 billionaires for the selected year
    top_20 = year_df.nlargest(20, 'net_worth')
    
    # Add flag emojis to names
    top_20['name_with_flag'] = top_20.apply(
        lambda row: f"{row['full_name']} {get_flag_emoji(row['iso3c'])} ", 
        axis=1
    )
    
    # Create horizontal bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_20['name_with_flag'],
        x=top_20['net_worth'],
        orientation='h',
        #text=top_20['net_worth'].round(1),
        #texttemplate='$%{text:.1f}B',
        #textposition='auto',
        hovertemplate='%{y}<br>$%{x:.1f}B<extra></extra>', 
        hoverlabel=dict(bgcolor='white', font_size=14, align='left'),
        marker_color='#4B2991'
    ))
    
    # Update layout
    fig.update_layout(
        title=None,
        xaxis=dict(
            title="Net Worth (Billions USD)",
            tickprefix="$",
            ticksuffix="B",
            tickformat=".1f"
        ),
        yaxis_title=None,
        showlegend=False,
        height=370,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor=PAPER_BGCOLOR,
        plot_bgcolor=PLOT_BGCOLOR
    )
    
    return fig
