"""
Callbacks for the wealth chart visualization.
"""
from dash import Input, Output, State
import dash
import json

def register_wealth_chart_callbacks(app, df):
    """Register callbacks for wealth chart."""
    @app.callback(
        [
            Output("year-slider", "value"),
            Output("wealth-chart", "figure"),
            Output("animation-interval", "disabled"),
            Output("play-button", "children"),
        ],
        [
            Input("play-button", "n_clicks"),
            Input("animation-interval", "n_intervals"),
            Input("year-slider", "value"),
            Input("selected-country", "children"),
        ],
        [
            State("year-slider", "max"),
            State("animation-interval", "disabled"),
        ],
    )
    def update_wealth_chart(n_clicks, n_intervals, selected_year,selected_country, max_year, is_paused):
        triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        
        # Handle play button logic
        if triggered_id == "play-button":
            if is_paused:
                return selected_year, dash.no_update, False, "Pause"
            else:
                return selected_year, dash.no_update, True, "Play"

        # Handle interval animation logic
        if triggered_id == "animation-interval":
            if not is_paused:
                next_year = min(selected_year + 1, max_year)
                if next_year == max_year:
                    return next_year, dash.no_update, True, "Play"
                selected_year = next_year

        is_paused = bool(is_paused)
                
        # Filter data and create visualization
        year_df = df[df['year'].dt.year == selected_year]
        from modules.visualizations import create_wealth_chart
        wealth_chart = create_wealth_chart(year_df,selected_country)
        
        return selected_year, wealth_chart, is_paused, "Pause" if not is_paused else "Play"
