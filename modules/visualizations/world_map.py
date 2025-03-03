"""
World map visualization for the Billionaires Dashboard.
"""
import plotly.graph_objects as go


def create_world_map(selected_year, view_type, bill_df, scatter_data):
    """Create the world map visualization."""
    # Get min/max values for color scaling
    min_val = bill_df[view_type].min()
    max_val = bill_df[view_type].max()
    
    # Adjust max value for percent_of_gdp
    if view_type == "billionaire_count":
        tab = "Billionaire Count"
    else:
        tab = "Wealth as a Percent of GDP"
        max_val = bill_df['percent_of_gdp'].quantile(0.90)
    
    # Filter data for selected year
    choropleth_data = bill_df[bill_df["year"] == selected_year]
    scatter_data_filtered = scatter_data[scatter_data["year"] == selected_year]

    # Filter data for only countries with data
    scatter_data_filtered = scatter_data_filtered.dropna(subset=[view_type])
  
    
    # Create figure with both choropleth and scatter traces
    fig = go.Figure()
    
    # Add choropleth trace
    fig.add_trace(
        go.Choropleth(
            locations=choropleth_data["iso3c"],
            z=choropleth_data[view_type],
            text=(
                choropleth_data["country_of_citizenship"]
                + f"<br>{tab}: "
                + choropleth_data[view_type].map(lambda x: f"{x:.2f}".rstrip("0").rstrip("."))
            ),
            colorscale="agsunset_r",
            zmin=min_val,
            zmax=max_val,
            colorbar=dict(
                title=tab,
                thickness=15,
                len=0.6,
                x=.9,
                y=0.5,
                yanchor='middle',
                titleside='right',
                ticks='outside'
            ),
            hoverinfo="text"
        )
    )

    # Scatter points only show up if there is billionaire data for that country, otherwise they are not there
    if not scatter_data_filtered.empty:
        fig.add_trace(
            go.Scattergeo(
                lat=scatter_data_filtered["lattitude"],
                lon=scatter_data_filtered["longitude"],
                text=(
                    scatter_data_filtered["country_of_citizenship"]
                    + f"<br>{tab}: "
                    + scatter_data_filtered[view_type].map(lambda x: f"{x:.2f}".rstrip("0").rstrip("."))
                ),
                mode="markers",
                marker=dict(
                    size=10,
                    color=scatter_data_filtered[view_type],
                    cmin=min_val,
                    cmax=max_val,
                    colorscale="agsunset_r",
                    colorbar=None,
                    line=dict(
                        color="black",
                        width=2
                    )
                ),
                hovertemplate="Country: %{text}<extra></extra>"
            )
        )
    
    # Update map projection and appearance
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="White",
        showcountries=True,
        showocean=True,
        oceancolor="LightBlue",
        showlakes=True,
        lakecolor="LightBlue",
        projection_rotation_lon=-98.5795,
        projection_rotation_lat=37.0902,
    )
    
    # Update layout
    fig.update_layout(
        margin=dict(l=0, r=90, t=0, b=0),
        coloraxis_colorbar=dict(title=tab),
        uirevision="true",
        clickmode="event"
    )
    
    
    return fig


if __name__ == "__main__":
    print("This module is not meant to be run directly")