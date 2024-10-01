import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout without data/visualizations
app.layout = dbc.Container([
    dbc.Row([  # Sidebar row
        dbc.Col([
            html.Div("Sidebar content here", style={'background-color': '#f8f9fa', 'padding': '20px', 'height': '100vh'})
        ], width=2),  # Sidebar takes 2 columns
        dbc.Col([  # Main content area takes 10 columns
            dbc.Row([  # Row for KPI cards
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 1", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="primary", inverse=True, style={'height': '150px'}), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 2", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="success", inverse=True, style={'height': '150px'}), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("KPI 3", className="card-title"),
                    html.H2("Placeholder Value", className="card-text")
                ]), color="danger", inverse=True, style={'height': '150px'}), width=4)
            ], className="mb-4"),  # Add margin-bottom to the KPI row
            dbc.Row([  # First row of visualization placeholders
                dbc.Col(dbc.Card(dbc.CardBody("Visualization 1 Placeholder"), style={'height': '400px'}), width=6),
                dbc.Col(dbc.Card(dbc.CardBody("Visualization 2 Placeholder"), style={'height': '400px'}), width=6),
            ], className="mb-4"),  # Add margin-bottom to the first visualization row
            dbc.Row([  # Second row of visualization placeholders
                dbc.Col(dbc.Card(dbc.CardBody("Visualization 3 Placeholder"), style={'height': '400px'}), width=12)
            ])
        ], width=10)
    ])
], fluid=True, style={'height': '100vh'})  # Set the container height to full viewport height

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
