import pandas as pd
import plotly.graph_objects as go

# Load the data (you'll need to replace this with your actual data source)
df = pd.read_csv('billionaire_data.csv')

# Filter the dataframe for a specific year (replace 2023 with your desired year)
year = 2023
df_filtered = df[df['year'] == year]

# Sort the filtered dataframe by net worth in descending order and take the top 30
top_30 = df_filtered.sort_values('net_worth', ascending=False).head(30)

# Create the column chart
fig = go.Figure(go.Bar(
    x=top_30['net_worth'],
    y=top_30['full_name'],
    orientation='h',
    marker=dict(color='skyblue', line=dict(color='darkblue', width=1))
))

# Customize the layout
fig.update_layout(
    title=f'Top 30 Billionaires by Net Worth in {year}',
    xaxis_title='Net Worth (in billions USD)',
    yaxis_title='Billionaire Names',
    height=800,
    width=1000,
    yaxis=dict(autorange="reversed")  # This will display the richest at the top
)

# Show the plot
fig.show()

# Optionally, save the plot as an HTML file
fig.write_html(f"top_30_billionaires_{year}.html")
