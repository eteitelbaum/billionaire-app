"""
Callbacks for the world map visualization.
"""
from dash import Input, Output, State
import dash
from modules.visualizations import create_world_map

def register_world_map_callbacks(app, bill_df, scatter_data):
    """Register callbacks for world map."""
    @app.callback(
        Output("choro-map", "figure"),
        [
            Input("year-slider", "value"),
            Input("switch-options", "value"),
        ]
    )
    def update_world_map(selected_year, view_type):
        """Update world map based on year and view type."""
        return create_world_map(selected_year, view_type, bill_df, scatter_data)
