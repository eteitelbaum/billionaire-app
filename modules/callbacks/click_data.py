from dash import Input, Output, State
from modules.visualizations import click_data as cd
import dash


def register_click_data_callbacks(app):
    @app.callback(
        Output("selected-country", "children"),
        [
            Input("choro-map", "clickData"),
            Input("map-container", "n_clicks")

        ])
    
    def update_selected_country(clickData,n_clicks):
        ctx = dash.callback_context

        if not ctx.triggered:
            return None

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'map-container':
            return None

        return cd.click_data_info(clickData)
        