"""
Configuration settings for the Billionaires Dashboard.
"""

# Visualization settings
CHART_HEIGHT = 400
MAP_HEIGHT = 350
TREEMAP_HEIGHT = 400

# Animation settings
ANIMATION_INTERVAL = 1000  # milliseconds

# Color settings
CHOROPLETH_COLORSCALE = "agsunset_r"
TREEMAP_COLORSCALE = "turbo" # not currently used 
OCEAN_COLOR = "LightBlue"
LAND_COLOR = "White"

# Map projection settings
MAP_ROTATION_LON = -98.5795
MAP_ROTATION_LAT = 37.0902

# Layout settings
MARGIN_NO_PAD = dict(l=0, r=0, t=0, b=0)
MARGIN_WITH_LEGEND = dict(l=0, r=90, t=0, b=0)

# Hover formatting
HOVER_MONEY_FORMAT = '$%{x:.2f}B'  # Two decimal places for hover

# Visual theme settings
PLOT_BGCOLOR = 'rgba(0,0,0,0)'  # Transparent background
PAPER_BGCOLOR = 'rgba(0,0,0,0)'  # Transparent paper/container background

# Layout spacing settings
CONTROLS_MARGIN_TOP = "mt-3"    # Bootstrap margin class for top spacing

# Control theme settings
SLIDER_STYLE = {
    "accentColor": "#D43F96",
    "--progress-color": "#D43F96",
    "border": "none",
    "padding": "0",
    "margin": "0"
}

PLAY_BUTTON_STYLE = {
    "backgroundColor": "#D43F96",
    "border": "none",
    "padding": "6px 12px",  # Adjust as needed
    "marginRight": "-10px"  # Negative margin to pull slider closer
}

# Remove the complex flex layout and use simpler positioning
CONTROLS_CONTAINER_STYLE = {
    "marginTop": "20px"  # Add some space above controls
}
