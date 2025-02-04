"""
Callbacks for the treemap visualization.
"""
from dash import Input, Output
from modules.visualizations import create_treemap

def register_treemap_callbacks(app, df):
    """Register callbacks for treemap."""
    @app.callback(
        Output('industrytreemap', 'figure'),
        Input('year-slider', 'value')
    )
    def update_treemap(year):
        """Update treemap based on selected year."""
        year_df = df[df['year'].dt.year == year]
        return create_treemap(year_df)
