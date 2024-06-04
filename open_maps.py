import os
from dotenv import load_dotenv
import requests
import webbrowser

# Load environment variables from .env file
load_dotenv()


def check_street_view_availability(lat, lon):
    api_key = os.getenv('GOOGLE_API_KEY')
    metadata_url = (
        f"https://maps.googleapis.com/maps/api/streetview/metadata?"
        f"location={lat},{lon}&key={api_key}"
    )
    response = requests.get(metadata_url)
    data = response.json()
    return data.get("status") == "OK"


def open_google_maps(lat, lon):
    api_key = os.getenv('GOOGLE_API_KEY')
    base_url = "https://www.google.com/maps"
    maps_url = f"{base_url}?q={lat},{lon}"

    if check_street_view_availability(lat, lon):
        street_view_url = f"{base_url}?cbll={lat},{lon}&layer=c"
        # Open Street View if available
        webbrowser.open_new(street_view_url)
    else:
        # Open Google Maps at the given latitude and longitude
        webbrowser.open_new(maps_url)


# Example usage 40.689429, -73.892922
latitude = 40.689429
longitude = -73.892922
open_google_maps(latitude, longitude)

