import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load the data
df = pd.read_csv('billionaire_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

# Define the layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Wealth Trends", href="/trends")),
            dbc.NavItem(dbc.NavLink("Data Download", href="/download")),
        ],
        brand="Billionaire Wealth Dashboard",
        color="primary",
        dark=True,
    ),
    dash.page_container
])

# Home page (existing visualization)
dash.register_page("home", path="/")

@dash.callback(
    Output("home-content", "children"),
    Input("year-dropdown", "value")
)
def update_home_page(selected_year):
    filtered_df = df[df['year'] == selected_year]
    top_30 = filtered_df.sort_values('net_worth', ascending=False).head(30)
    
    fig = px.bar(top_30, x='net_worth', y='full_name', orientation='h',
                 title=f'Top 30 Billionaires by Net Worth in {selected_year}')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    
    return dcc.Graph(figure=fig)

# Wealth Trends page
dash.register_page("trends", path="/trends")

@dash.callback(
    Output("trends-chart", "figure"),
    Input("billionaire-search", "value")
)
def update_trends_chart(selected_billionaires):
    if not selected_billionaires:
        return px.line()
    
    filtered_df = df[df['full_name'].isin(selected_billionaires)]
    fig = px.line(filtered_df, x='year', y='net_worth', color='full_name',
                  title='Billionaire Wealth Trends Over Time')
    return fig

# Data Download page
dash.register_page("download", path="/download")

@dash.callback(
    Output("download-link", "href"),
    Input("download-button", "n_clicks")
)
def update_download_link(n_clicks):
    if n_clicks is None:
        return ""
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)