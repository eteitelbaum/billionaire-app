import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the data
df = pd.read_csv('data/billionaires_with_country_data.csv')

# Preprocess the data
df['year'] = pd.to_datetime(df['year'], format='%Y')
df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout without data/visualizations
app.layout = dbc.Container([
    dbc.Row([  # Main content area
        dbc.Col([  
            dbc.Row([  # KPI cards row
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 1", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="primary", inverse=True, style={'height': '100px'}), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 2", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="success", inverse=True, style={'height': '100px'}), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 3", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="danger", inverse=True, style={'height': '100px'}), width=4)
            ], className="mb-4"),
            
            dbc.Row([  # Visualization row
                dbc.Col(dbc.Card(dbc.CardBody([  
                    dcc.Graph(
                        id="wealth-chart",
                        config={
                            'displayModeBar': False,  # This removes the plotly controls
                            'showTips': False
                        }
                    ),
                ]), style={'height': '400px'}), width=6),
                
                dbc.Col(dbc.Card(dbc.CardBody("Visualization 2 Placeholder"), 
                    style={'height': '400px'}), width=6),
            ], className="mb-4"),
            
            dbc.Row([  # Bottom row
                dbc.Col(dbc.Card(dbc.CardBody("Bottom Card Placeholder"), 
                    style={'height': '400px'}), width=12)
            ], className="mb-4"),

            # New row for slider and controls
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
                        dbc.Button("Play", id="play-button", className="mt-3"),
                        dcc.Interval(id="animation-interval", interval=1000, n_intervals=0, disabled=True)
                    ], style={'textAlign': 'center'})
                ], width=12)
            ])
        ], width=12)
    ])
], fluid=True, style={'height': '100vh'})

# Add these functions after the layout but before app.run_server:

def get_flag_emoji(iso3):
    if pd.isna(iso3) or len(iso3) != 3:
        return ''
    iso2 = iso3[:2]
    return ''.join(chr(ord(c) + 127397) for c in iso2)

@callback(
    Output("wealth-chart", "figure"),
    Input("year-slider", "value")
)
def update_chart(selected_year):
    # Filter data for the selected year
    year_df = df[df['year'].dt.year == selected_year]
    
    # Get top 30 billionaires for this year
    top_30 = year_df.nlargest(30, 'net_worth')
    
    # Add flag emojis to names
    top_30['name_with_flag'] = top_30.apply(lambda row: f"{row['full_name']} {get_flag_emoji(row['iso3c'])} ", axis=1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_30['name_with_flag'],
        x=top_30['net_worth'],
        orientation='h',
        hovertemplate='$%{x:.2f}B<extra></extra>',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            align='left'
        )
    ))
    
    fig.update_layout(
        xaxis_title="Net Worth (USD)",
        #yaxis_title="Billionaire",
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=10),
            constrain='domain',
            nticks=len(top_30),
            showticklabels=True,
        ),
        bargap=0.1,  # Gap between bars (0 to 1)
        height=400,  # Might need to adjust if using autosize
        autosize=True,  # Makes the plot responsive
        margin=dict(l=0, r=0, t=0, b=20),  # Minimal margins
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',  # Optional: transparent background
        plot_bgcolor='rgba(0,0,0,0)',    # Optional: transparent plot area
        hoverdistance=100,  # Increases hover sensitivity
        hovermode='y'  # Makes hover work better for horizontal bars
    )
    
    # Option 3: Break long names into multiple lines
    top_30['name_with_flag'] = top_30.apply(
        lambda row: f"{get_flag_emoji(row['iso3c'])} {row['full_name'][:20]}<br>{row['full_name'][20:]}", 
        axis=1
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

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
