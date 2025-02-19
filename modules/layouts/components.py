"""
Individual layout components for the Billionaires Dashboard.
"""
from dash import dcc, html
import dash_bootstrap_components as dbc
from modules.config import (
    PLAY_BUTTON_STYLE, SLIDER_STYLE,
    CONTROLS_MARGIN_TOP
)

def create_title_row():
    """Create the title row."""
    return dbc.Row([
        dbc.Col(html.H2(
            "The Oligarchy Atlas", 
            className="text-left mb-2"), 
            width=12, 
            style={"color": "#D43F96"})
    ])

def create_visualization_row():
    """Create the row containing wealth chart and world map."""
    return dbc.Row([
        # Wealth Chart Column
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        id="wealth-chart",
                        config={
                            'displayModeBar': False,
                            'showTips': False
                        }
                    ),
                ]),
                style={'height': '400px'}
            ),
            width=6
        ),
        
        # World Map Column
        dbc.Col(
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        dbc.RadioItems(
                            options=[
                                {"label": "Billionaire Count", "value": "billionaire_count"},
                                {"label": "Wealth as % of GDP", "value": "percent_of_gdp"},
                            ],
                            value="billionaire_count",
                            inline=True,
                            id="switch-options",
                            className="pt-2 pe-2",
                            style={"float": "right"},
                        ),
                    ], width=12, className="text-end"),
                ], className="g-0"),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            id="choro-map",
                            config={'displayModeBar': False},
                            style={"height": "350px"},
                        ),
                    ], width=12),
                ], className="g-0"),
            ], style={'height': '400px'}),
            width=6
        ),
    ], className="mb-4")

def create_treemap_row():
    """Create the treemap row."""
    return dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='industrytreemap')
                ]),
                style={'height': '400px'}
            ),
            width=12
        )
    ])

def create_controls_row(min_year, max_year):
    """Create the controls row with slider and play button."""
    return dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([  # Play button first
                    dbc.Button(
                        "Play",
                        id="play-button",
                        style=PLAY_BUTTON_STYLE
                    ),
                ], width=2),  # Take up 1/12 of the row
                dbc.Col([  # Then slider
                    dcc.Slider(
                        id="year-slider",
                        min=min_year,
                        max=max_year,
                        value=min_year,
                        marks={str(year): str(year) for year in range(min_year, max_year + 1)},
                        step=None
                    ),
                ], width=10),  # Take up 11/12 of the row
                dcc.Interval(
                    id="animation-interval",
                    interval=1000,
                    n_intervals=0,
                    disabled=True
                )
            ], align="center")  # Vertically center the items
        ], width=12)
    ], className=CONTROLS_MARGIN_TOP)
