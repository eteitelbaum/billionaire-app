# Standard library imports
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

# Third-party imports
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# ------------------------
# Data Loading & Preprocessing
# ------------------------

from modules.data import load_and_preprocess_data
#from modules.visualizations import create_wealth_chart, create_world_map
from modules.callbacks import (
    register_wealth_chart_callbacks,
    register_world_map_callbacks,
    register_treemap_callbacks,
)
from modules.layouts import create_layout
from modules.callbacks import click_data as cd

# Load data
df, bill_df, scatter_data = load_and_preprocess_data()

# ------------------------
# Helper Functions
# ------------------------
def get_flag_emoji(iso3):
    """Convert ISO3 country code to flag emoji."""
    if pd.isna(iso3) or len(iso3) != 3:
        return ''
    iso2 = iso3[:2]
    return ''.join(chr(ord(c) + 127397) for c in iso2)

# ------------------------
# App Initialization
# ------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ------------------------
# Layout
# ------------------------
app.layout = create_layout(df)

# Register callbacks
register_wealth_chart_callbacks(app, df)
register_world_map_callbacks(app, bill_df, scatter_data)
register_treemap_callbacks(app, df)
cd.register_click_data_callbacks(app)

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
