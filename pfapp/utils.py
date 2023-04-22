
from .models import *
import pandas as pd

import requests
import folium
from .tasks import worker_function
import random
from geopy import Point
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="test1")


def gym_details(lat,long):
    gym_name = []
    gym_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "gym",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        gym_name.append(i['name'])
        gym_loc.append(i['location'])
    return gym_name, gym_loc

def rest_details(lat,long):
    rest_name = []
    rest_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "restaurants",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        rest_name.append(i['name'])
        rest_loc.append(i['location'])
    return rest_name, rest_loc


def coffee_details(lat,long):
    coffee_name = []
    coffee_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "coffee",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        coffee_name.append(i['name'])
        coffee_loc.append(i['location'])
    return coffee_name, coffee_loc

def shopping_details(lat,long):
    shopping_name = []
    shopping_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "shopping",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        shopping_name.append(i['name'])
        shopping_loc.append(i['location'])
    return shopping_name, shopping_loc


def parks_details(lat,long):
    parks_name = []
    parks_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "parks",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        parks_name.append(i['name'])
        parks_loc.append(i['location'])
    return parks_name, parks_loc

def drinks_details(lat,long):
    drinks_name = []
    drinks_loc = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    params = {
        "query": "drinks",
        "ll": str(str(lat)+','+str(long)),
        "open_now": "true",
        "sort": "DISTANCE",
        "radius": "6000"
    }
    response = requests.request("GET", url, params=params, headers=headers)
    result = response.json()

    a = result['results']

    for i in a:
        drinks_name.append(i['name'])
        drinks_loc.append(i['location'])
    return drinks_name, drinks_loc