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

df = pd.read_csv('data/billionaires_with_country_data.csv')
df['year'] = pd.to_datetime(df['year'], format='%Y')
df = df[df['year'].dt.year >= 2000]
df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')
bill_df = pd.read_csv('data/billionaire_count_and_wealth_data.csv')
bill_df = bill_df[bill_df['year'] >= 2000]
scatter_data = pd.read_csv('data/scatter_geo_data_complete.csv')
scatter_data = scatter_data[scatter_data['year'] >= 2000]

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
# Layout
# ------------------------
app.layout = dbc.Container([
    # Add title row
    dbc.Row([
        dbc.Col(html.H2("Billionaire App", className="text-center mb-2"), width=12)
    ]),     
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
                
                dbc.Col(dbc.Card(dbc.CardBody([
                    #html.H1("Billionaire Count and Wealth as % of GDP"),
                    #html.P("Choose visualization type:"), 
                    dbc.Tabs(
                    [
                        dbc.Tab(label="Billionaire Count", tab_id="billionaire_count"),
                        dbc.Tab(label="Wealth as % of GDP", tab_id="percent_of_gdp"),
                    ],
                    id="tabs",
                    active_tab="billionaire_count",
                ),
                dcc.Graph(id="choro-map",
                    config={
                        'displayModeBar': False  
                        },),
                    ]), 
                    style={'height': '400px'}), width=6),
            ], className="mb-4"),
            
            dbc.Row([  # Bottom row
                dbc.Col(dbc.Card(dbc.CardBody([
                    dcc.Graph(id='industrytreemap')
                ]),
                    style={'height': '400px'}), width=12)
            ]),

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
        ], fluid=True)

# Add these functions after the layout but before app.run_server:

def get_flag_emoji(iso3):
    if pd.isna(iso3) or len(iso3) != 3:
        return ''
    iso2 = iso3[:2]
    return ''.join(chr(ord(c) + 127397) for c in iso2)


@app.callback(
    [
        Output("year-slider", "value"),
        Output("wealth-chart", "figure"),
        Output("choro-map", "figure"),
        Output("animation-interval", "disabled"),
        Output("play-button", "children"),
    ],
    [
        Input("play-button", "n_clicks"),
        Input("animation-interval", "n_intervals"),
        Input("year-slider", "value"),
        Input("tabs", "active_tab"),
    ],
    [
        State("year-slider", "max"),
        State("animation-interval", "disabled"),
    ],
)

def update_visualizations(n_clicks,n_intervals,selected_year, active_tab, max_year, is_paused):
    triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
    # Handle play button logic
    if triggered_id == "play-button":
        if is_paused:
            return selected_year, dash.no_update, dash.no_update, False, "Pause"
        else:
            return selected_year, dash.no_update, dash.no_update, True, "Play"


    # Handle interval animation logic
    if triggered_id == "animation-interval":
        if not is_paused:
            next_year = min(selected_year + 1, max_year)
            if next_year == max_year:
                return next_year, dash.no_update, dash.no_update, True, "Play"
            selected_year = next_year
            
    # Filter data for the selected year
    year_df = df[df['year'].dt.year == selected_year]
    
    # Get top 30 billionaires for this year
    top_20 = year_df.nlargest(20, 'net_worth')

    # Add flag emojis to names
    top_20['name_with_flag'] = top_20.apply(lambda row: f"{row['full_name']} {get_flag_emoji(row['iso3c'])} ", axis=1)
    
    wealth_chart = go.Figure()
    wealth_chart.add_trace(go.Bar(
        y=top_20['name_with_flag'],
        x=top_20['net_worth'],
        orientation='h',
        hovertemplate='$%{x:.2f}B<extra></extra>',
        hoverlabel=dict(bgcolor='white', font_size=14, align='left')
    ))

    wealth_chart.update_layout(
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
    wealth_chart.update_yaxes(
        ticksuffix=' ',
        automargin=True
    )
    
    min_val = bill_df[active_tab].min()
    max_val = bill_df[active_tab].max()
    
    choropleth_data = bill_df[bill_df["year"] == selected_year]
    scatter_data_filtered = scatter_data[scatter_data["year"] == selected_year]
    
    if active_tab == "billionaire_count":
        tab = "Billionaire Count"
    else:
        tab = "Wealth as a Percent of GDP"
        max_val = bill_df['percent_of_gdp'].quantile(0.90)
        
    choro_map = go.Figure()
    choro_map.add_trace(
        go.Choropleth(
            locations = choropleth_data["iso3c"],
            z = choropleth_data[active_tab],
            text=(
                choropleth_data["country_of_citizenship"]
                + f"<br>{tab}: "
                + choropleth_data[active_tab].astype(str)),
            colorscale = "agsunset_r",
            zmin = min_val,
            zmax = max_val,
            colorbar_title = tab,
            hoverinfo = "text"
            ))
    
    choro_map.add_trace(
        go.Scattergeo(
            lat=scatter_data_filtered["lattitude"],
            lon=scatter_data_filtered["longitude"],
            text=(
                scatter_data_filtered["country_of_citizenship"]
                + f"<br>{tab}: "
                + scatter_data_filtered[active_tab].astype(str)
            ),
            mode="markers",
            marker=dict(
                size=10,
                color = scatter_data_filtered[active_tab],
                cmin = min_val,
                cmax = max_val,
                colorscale = "agsunset_r",
                line = dict(
                    color = "black",
                    width = 2
                )), 
            hovertemplate="Country: %{text}<extra></extra>"))
    
    choro_map.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="White",
        showcountries=True,
        showocean=True, 
        oceancolor="LightBlue",
        showlakes=True, 
        lakecolor="Blue",
    )
    
    choro_map.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title=tab),
    )

    return selected_year, wealth_chart, choro_map, is_paused, "Pause" if not is_paused else "Play"

@app.callback(
    Output('industrytreemap', 'figure'),
    #Input('country-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_graph(#selected,
                 year):
    #filtered_df = df[df['country_of_citizenship'].isin(selected)] # filter selected country
    #filtered_df = filtered_df[filtered_df['year'] == year].query('industry == industry') # filter selected year
    filtered_df = df[df['year'].dt.year == year].dropna(subset=['industry'])
    fig = px.treemap(
        filtered_df,
        path=[px.Constant("all"),
              #"country_of_citizenship",
              "industry", "full_name"], # variables outside -> inside
        values="net_worth", # count based on net worth
        color = 'industry', # color based on industry
        maxdepth = 3)

    fig.update_layout(
        height=400,  # Might need to adjust if using autosize
        #autosize=True,  # Makes the plot responsive
        margin=dict(l=0, r=0, t=0, b=30),  # Minimal margins
        #paper_bgcolor='rgba(0,0,0,0)',  # Optional: transparent background
        #plot_bgcolor='rgba(0,0,0,0)',  # Optional: transparent plot area
    )

    return fig

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    app.run_server(debug=True)