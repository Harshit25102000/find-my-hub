
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


import random
from geopy import Point
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="test1")
import urllib.parse
import numpy as np
import sklearn
import json
import requests
from celery import shared_task
from django.core.mail import send_mail
from django.core import mail
from django.core import serializers
from .models import *
num=100
User = get_user_model()

import pandas as pd
import pickle
from .models import *

"""____________________________________________All get functions_________________________________________________"""

def getgym(df):
    gymarray = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "gym",
            "ll": str(str(df['latitude'][i])+','+str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        gymarray.append(ans)
    return gymarray

def getrest(df):
    restarray = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "restaurants",
            "ll": str(str(df['latitude'][i]) + ',' + str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        restarray.append(ans)
    return restarray

def getcoffee(df):
    coffeearray = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "coffee",
            "ll": str(str(df['latitude'][i]) + ',' + str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        coffeearray.append(ans)
    return coffeearray

def getshopping(df):
    shoppingarray=[]

    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "shopping",
            "ll": str(str(df['latitude'][i]) + ',' + str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        shoppingarray.append(ans)
    return shoppingarray

def getparks(df):
    parksarray = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "parks",
            "ll": str(str(df['latitude'][i]) + ',' + str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        parksarray.append(ans)
    return parksarray

def getdrinks(df):
    drinksarray = []
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Ov/Qqhpqdc7yJYNb/RBkuHG9VPwR1zr1H1S5NEJxh+A="
    }

    for i in range(num):
        params = {
            "query": "drinks",
            "ll": str(str(df['latitude'][i]) + ',' + str(df['longitude'][i])),
            "open_now": "true",
            "sort": "DISTANCE",
            "radius": "10000"
        }
        response = requests.request("GET", url, params=params, headers=headers)
        result = response.json()
        ans = len(result['results'])
        drinksarray.append(ans)
    return drinksarray

def latlong(address):
    import requests
    import urllib.parse

    address = str(address)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()
    lat=(response[0]["lat"])
    long=(response[0]["lon"])
    ls=[]
    ls.append(lat)
    ls.append(long)
    return ls

def generate_point(center: Point, radius: int):
    radius_in_kilometers = radius * 1e-3
    random_distance = random.random() * radius_in_kilometers
    random_bearing = random.random() * 360
    return geodesic(kilometers=random_distance).destination(center, random_bearing)

def getallpos(latitude,longitude):


    radius = 5000
    center = Point(latitude, longitude)

    points = []
    for i in range(num):
        a = ((generate_point(center, radius)))
        points.append(a)

    table = pd.DataFrame(columns=["latitude","longitude"])
    latarray=[]
    longarray=[]
    for point in points:
        latarray.append(point.latitude)
        longarray.append(point.longitude)
    table["latitude"]=latarray
    table["longitude"]=longarray

    return table



import joblib
@shared_task(bind=True)
def worker_function(self,args):
    print("---------------------task running---------------------")
    print("didnt find in db")
    my_string = args
    split_string = my_string.split('&', 1)
    address = split_string[0]
    email = split_string[1] if len(split_string) > 1 else ""
    print(email)

    ls = latlong(address)
    latitude = ls[0]
    longitude = ls[1]

    print(latitude, longitude)
    df = getallpos(latitude, longitude)

    print(df)
    gymarray = getgym(df)
    restarray = getrest(df)
    coffeearray = getcoffee(df)
    df["gyms"] = gymarray
    df["restaurants"] = restarray
    df["coffee"] = coffeearray
    shoppingarray = getshopping(df)
    parksarray = getparks(df)
    drinksarray = getdrinks(df)
    df["shopping"] = shoppingarray
    df["parks"] = parksarray
    df["drinks"] = drinksarray
    print(df)
    model = joblib.load('amenity_classifier_py.sav')
    x = df.drop(['latitude', 'longitude'], axis='columns')
    y = model.predict(x)
    df["cluster"] = y
    print(df)
    user = User.objects.get(email=email)

    info = people_info.objects.filter(user=user).first()
    user_cluster = info.cluster
    if user_cluster == 2:
        rslt_df = df[(df['cluster'] == 1)]
    elif user_cluster == 1:
        rslt_df = df[(df['cluster'] == 2)]
    elif user_cluster == 0:
        rslt_df = df[(df['cluster'] == 0)]

    # Create a new instance of the Dataframe model and set the dataframe
    dataframe = Dataframe(user=user, area=address)
    dataframe.set_dataframe(rslt_df)
    dataframe.save()

    message = f"We are done with your request to process for given address which was {address}. Now you can visit the website and when you will search for this address you will get the results instantly "
    print(email)

    results = send_mail(
        'Your ML Model is Created',
        message,
        'harshit25102000@gmail.com',
        [email],
        fail_silently=False,
    )
    print(results)
    print("task ended")

