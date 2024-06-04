import json
import requests
import webbrowser


def load_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config


def check_street_view_availability(lat, lon, api_key):
    metadata_url = (
        f"https://maps.googleapis.com/maps/api/streetview/metadata?"
        f"location={lat},{lon}&key={api_key}"
    )
    response = requests.get(metadata_url)
    data = response.json()
    return data.get("status") == "OK"


def open_google_maps(lat, lon, api_key):
    base_url = "https://www.google.com/maps"
    maps_url = f"{base_url}?q={lat},{lon}"

    if check_street_view_availability(lat, lon, api_key):
        street_view_url = f"{base_url}?cbll={lat},{lon}&layer=c"
        # Open Street View if available
        webbrowser.open_new(street_view_url)
    else:
        # Open Google Maps at the given latitude and longitude
        webbrowser.open_new(maps_url)


# Load configuration from JSON file
config = load_config(r"C:\Users\nadav.k\Documents\DS\rep\api_key.json")

# Example usage
latitude = 40.748817
longitude = -73.985428
google_api_key = config.get('GOOGLE_API_KEY')
open_google_maps(latitude, longitude, google_api_key)
