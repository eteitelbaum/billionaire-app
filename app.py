# Standard library imports
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

# Third-party imports
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# ------------------------
# Data Loading & Preprocessing
# ------------------------
def load_and_preprocess_data():
    """Load and preprocess the billionaires dataset."""
    df = pd.read_csv('data/billionaires_with_country_data.csv')
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')
    return df

df = load_and_preprocess_data()

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

# ------------------------
# Layout Components
# ------------------------
def create_visualization_row():
    """Create the row containing main visualizations."""
    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            dcc.Graph(
                id="wealth-chart",
                config={'displayModeBar': False, 'showTips': False}
            ),
        ]), style={'height': '48vh'}), width=6),
        dbc.Col(dbc.Card(
            dbc.CardBody("Visualization 2 Placeholder"), 
            style={'height': '48vh'}
        ), width=6),
    ], className="mb-3")

# ------------------------
# Layout
# ------------------------
app.layout = dbc.Container([
    # Add title row
    dbc.Row([
        dbc.Col(html.H2("Billionaire App", className="text-center mb-2"), width=12)
    ]),
    
    dbc.Row([  # Main content area
        dbc.Col([  
            create_visualization_row(),
            
            dbc.Row([  # Bottom row
                dbc.Col(dbc.Card(dbc.CardBody("Bottom Card Placeholder"), 
                    style={'height': '37vh'}), width=12)
            ], className="mb-1"),  # Keep this small margin

            # Controls row
            dbc.Row([
                dbc.Col([
                    dcc.Slider(
                        id="year-slider",
                        min=df['year'].dt.year.min(),
                        max=df['year'].dt.year.max(),
                        value=df['year'].dt.year.min(),
                        marks={str(year): str(year) for year in range(df['year'].dt.year.min(), df['year'].dt.year.max()+1)},
                        step=None
                    ),
                    html.Div([
                        dbc.Button("Play", id="play-button", className="mt-2"),
                        dcc.Interval(id="animation-interval", interval=1000, n_intervals=0, disabled=True)
                    ], style={'textAlign': 'center'})
                ], width=12)
            ])
        ], width=12)
    ])
], fluid=True, style={
    'height': '98vh',
    'padding': '1vh',
    'display': 'flex',
    'flexDirection': 'column'
})

# ------------------------
# Callbacks
# ------------------------
@callback(
    Output("wealth-chart", "figure"),
    Input("year-slider", "value")
)
def update_chart(selected_year):
    """Update the wealth chart based on the selected year."""
    # Filter data for the selected year
    year_df = df[df['year'].dt.year == selected_year]
    
    # Get top 30 billionaires for this year
    top_30 = year_df.nlargest(30, 'net_worth')
    
    # Create and configure the figure
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_30.apply(
            lambda row: f"{row['full_name']} {get_flag_emoji(row['iso3c'])}",
            axis=1
        ),
        x=top_30['net_worth'],
        orientation='h',
        hovertemplate='$%{x:.2f}B<extra></extra>',
        hoverlabel=dict(bgcolor='white', font_size=14, align='left')
    ))
    
    # Update layout settings
    fig.update_layout(
        xaxis_title="Net Worth (USD)",
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=9),
            constrain='domain',
            showticklabels=True,
        ),
        bargap=0.2,
        height=400,
        autosize=True,
        margin=dict(l=200, r=20, t=10, b=30),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hoverdistance=100,
        hovermode='y'
    )
    
    # Additional layout adjustments
    fig.update_yaxes(
        ticksuffix=' ',
        automargin=True
    )
    
    return fig

@callback(
    Output("year-slider", "value"),
    Output("animation-interval", "disabled"),
    Input("play-button", "n_clicks"),
    Input("animation-interval", "n_intervals"),
    Input("year-slider", "value"),
    prevent_initial_call=True
)
def control_animation(n_clicks, n_intervals, current_year):
    triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "play-button":
        return current_year, False
    elif triggered_id == "animation-interval":
        next_year = min(current_year + 1, df['year'].dt.year.max())
        if next_year == df['year'].dt.year.max():
            return next_year, True
        return next_year, False
    else:
        return current_year, True

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
