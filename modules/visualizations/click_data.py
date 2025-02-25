def click_data_info(clickData):
    if clickData and isinstance(clickData, dict) and 'points' in clickData:
        selected_country = clickData['points'][0].get('text')
        country = selected_country.split('<br>')[0]
        if "Billionaire Count: nan" in selected_country or "Wealth as a Percent of GDP: nan" in selected_country:
            return None
        return country
    else:
        return None