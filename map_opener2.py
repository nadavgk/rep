import json
import streamlit as st
import requests
import webbrowser


def load_config(file_path):
    '''
    Loads the google API key from a json file
    :param file_path: path to json file with google API key
    :return: if a valid path to a json file was given and the json file has a valid API key it will return it. Else doesn't return
    '''
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: JSON configuration file not found. Google maps opened without street view.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON configuration file is not valid. Google maps opened without street view.")
        return None


def check_street_view_availability(lat, lon, api_key):
    '''
    connectes to google cloud streetview API's metadata and checks for street view availability in the given coordinates
    :param lat: Latitude
    :param lon: Longtitude
    :param api_key: google API-key given from json file used in: load_config()
    :return:
    '''
    metadata_url = (
        f"https://maps.googleapis.com/maps/api/streetview/metadata?"
        f"location={lat},{lon}&key={api_key}"
    )
    response = requests.get(metadata_url)
    data = response.json()
    return data.get("status") == "OK"


def open_google_maps(lat, lon, api_key):
    '''
    opens google maps on the web browser on the given coordinates with streetview if its available, if not only the map on the location is given
    :param lat:
    :param lon:
    :param api_key:
    :return:
    '''
    base_url = "https://www.google.com/maps"
    maps_url = f"{base_url}?q={lat},{lon}"

    if api_key and check_street_view_availability(lat, lon, api_key):
        street_view_url = f"{base_url}?cbll={lat},{lon}&layer=c"
        # Open Street View if available
        webbrowser.open_new(street_view_url)
    else:
        # Open Google Maps at the given latitude and longitude
        webbrowser.open_new(maps_url)


def find_nearby_places(lat, lon, place_type, api_key):
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&radius=1500&type={place_type}&key={api_key}"
    )
    response = requests.get(places_url)
    places_data = response.json()
    if places_data.get("status") == "OK":
        return places_data.get("results")
    else:
        st.error(f"Error finding nearby places: {places_data.get('status')} - {places_data.get('error_message')}")
        return []

def execute_map_opener(file_path, lat, lon):

    config = load_config(file_path)
    if config:
        google_api_key = config.get('GOOGLE_API_KEY')
        open_google_maps(lat, lon, google_api_key)
    else:
        open_google_maps(lat, lon, None)


# Load configuration from JSON file
jason_path = r"C:\Users\nadav.k\Documents\DS\rep\api_key.json"
# jason_path = r"C:\Users\nadav.k\Documents\DS\rep\api_key.json"
# config = load_config(r"C:\Users\nadav.k\Documents\DS\rep\api_key.json")

# Example usage 31.976317, 34.883420
lat = 31.976317
lon = 34.883420

# execute_map_opener(jason_path,lat,lon)

config = load_config(jason_path)
google_api_key = config.get('GOOGLE_API_KEY')

if config:
    google_api_key = config.get('GOOGLE_API_KEY')
    open_google_maps(lat, lon, google_api_key)

    # Find nearby gas stations
    nearby_gas_stations = find_nearby_places(lat, lon, "gas_station", google_api_key)
    print("Nearby Gas Stations:")
    for station in nearby_gas_stations:
        print(station["name"], "-", station["vicinity"])

    # Find nearby restaurants
    nearby_restaurants = find_nearby_places(lat, lon, "restaurant", google_api_key)
    print("\nNearby Restaurants:")
    for restaurant in nearby_restaurants:
        print(restaurant["name"], "-", restaurant["vicinity"])
else:
    open_google_maps(lat, lon, None)  # Open map without Street View