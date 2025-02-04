"""
Main layout configuration for the Billionaires Dashboard.
"""
import dash_bootstrap_components as dbc
from .components import (
    create_title_row,
    create_visualization_row,
    create_treemap_row,
    create_controls_row
)

def create_layout(df):
    """Create the main layout of the application."""
    # Get min and max years for the slider
    min_year = df['year'].dt.year.min()
    max_year = df['year'].dt.year.max()
    
    return dbc.Container([
        # Title
        create_title_row(),
        
        # Visualizations
        create_visualization_row(),
        
        # Treemap
        create_treemap_row(),
        
        # Controls
        create_controls_row(min_year, max_year)
    ], fluid=True)
