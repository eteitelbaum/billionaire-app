"""
Data loading and preprocessing functionality for the Billionaires Dashboard.
"""
import pandas as pd
import os

def load_and_preprocess_data():
    """Load and preprocess all required datasets."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load main billionaires dataset with low_memory=False to avoid dtype warning
    df = pd.read_csv(
        os.path.join(current_dir, 'billionaires_with_country_data.csv'),
        low_memory=False
    )
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df = df[df['year'].dt.year >= 2000]
    df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')

    # Load billionaire counts and wealth data
    bill_df = pd.read_csv(os.path.join(current_dir, 'billionaire_count_and_wealth_data.csv'))
    bill_df = bill_df[bill_df['year'] >= 2000]

    # Load geographical data
    scatter_data = pd.read_csv(os.path.join(current_dir, 'scatter_geo_data_complete.csv'))
    scatter_data = scatter_data[scatter_data['year'] >= 2000]

    return df, bill_df, scatter_data

def get_flag_emoji(iso3):
    """Convert ISO3 country code to flag emoji."""
    if pd.isna(iso3) or len(iso3) != 3:
        return ''
    iso2 = iso3[:2]
    return ''.join(chr(ord(c) + 127397) for c in iso2)
