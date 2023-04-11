from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import pandas as pd
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import requests
import folium
from .tasks import worker_function
import random
from geopy import Point
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="test1")
import urllib.parse
import numpy as np
import sklearn

num=5
User = get_user_model()

import pandas as pd
import pickle
from .models import *
# Create your views here.
def index(request):

    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def handle_signup(request):
    if request.method == 'POST':

        try:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, 'passwords do not match')
                return redirect('signup')

            if '@' not in email:
                messages.error(request, 'Enter a valid email address')
                return redirect('signup')

            user = User.objects.filter(email=email).first()

            if user:
                messages.error(request, 'Account already exists with this Email ')
                return redirect('signup')

            siteuser = User.objects.create_user(email, password1)
            siteuser.save()
            messages.success(request, 'Account created successfully! Please login using your credentials')
            return redirect('login')

        except:
            messages.success(request, 'Error creating account')
            return redirect('signup')
    else:
        return HttpResponse('404 Not Found')


def loginpage(request):
    return render(request, 'login.html')

def handle_login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']

        if '@' not in email:
            messages.error(request, 'Enter a valid email address')
            return redirect('login')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Account logged in successfully")

            return redirect('homepage')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('login')
    else:
        return HttpResponse("Not Allowed")

@login_required(login_url='/login/')
def homepage(request):
    user= request.user
    info = people_info.objects.filter(user=user).first()
    if info is None:
        return render(request,"user_info.html")
    return render(request, 'homepage.html')
import joblib


@login_required(login_url='/login/')
def handle_user_info(request):

    if request.user.is_authenticated:
        if request.method == 'POST':

            arr=[]
            coffee=request.POST['coffee']
            cook=request.POST['cook']
            drink=request.POST['drink']
            eating_out=request.POST['eating_out']
            exercise=request.POST['exercise']
            pay_meal=request.POST['pay_meal']

            arr.append(coffee)
            arr.append(cook)
            arr.append(drink)
            arr.append(eating_out)
            arr.append(exercise)
            arr.append(pay_meal)


            model=joblib.load('people_classifier_py.sav')

            ans=model.predict([arr])
            val=int(ans[0])
            info=people_info.objects.create(user=request.user,coffee=coffee,cook=cook,drink=drink,
            eating_out=eating_out,
            exercise=exercise,pay_meal=pay_meal,cluster=val)
            info.save()
            
            return redirect('homepage')

        else:
            return HttpResponse('Not Allowed')

    else:
        return HttpResponse('PLease Login')

from geopy.geocoders import Nominatim
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

@login_required(login_url='/login/')
def handle_input_name(request):
    print(request.method)
    if request.method == 'POST':


        address = request.POST['key']
        val = request.POST['hiddenInput']
        print(val)
        print(type(val))
        dataframes = Dataframe.objects.filter(user=request.user,area=address).first()



        #try:
        if val=="on" and dataframes:
            # Retrieve the dataframe from the database
            print("running")
            ls = latlong(address)
            latitude = ls[0]
            longitude = ls[1]
            retrieved_dataframe = dataframes.get_dataframe()
            rslt_df=retrieved_dataframe

            print(rslt_df)
            addr = []
            lat = rslt_df['latitude'].tolist()
            long = rslt_df['longitude'].tolist()
            print(lat)
            print(long)
            for i in range(len(lat)):
                try:
                    strlatlong = str(str(lat[i]) + ',' + str(long[i]))
                    location = geolocator.reverse(strlatlong)
                    addr.append(location.address)
                except:
                    addr.append('Could Not found address')
            print(addr)
            m = folium.Map(location=[latitude, longitude], zoom_start=10)
            for i in range(len(lat)):
                folium.Marker(location=[lat[i], long[i]], tooltip='click for location', popup=str(lat[i]) + ',' +
                                                                                              str(long[i])).add_to(m)
            m = m._repr_html_()
            points = zip(lat, long, addr)

            context = {'m': m, 'points': points}
            return render(request, 'map.html', context)

        else:

            email = str(request.user.email)
            args = str(str(address) + '&' + str(email))
            worker_function.delay(args)
            messages.error(request, "Processing for your request is started , once completed you will get an email")
            return redirect('homepage')




        """except Exception as e:
            print(e)
            messages.error(request, "Sorry we can't find this address , please use latitude and longitude to "
            "use our services")
            return redirect('homepage')"""


    else:   
        return HttpResponse("Not Allowed")

from geopy.geocoders import Nominatim
@login_required(login_url='/login/')
def handle_latlong(request):
    if request.method == 'POST':
        latitude=request.POST['latitude']
        longitude=request.POST['longitude']
        val=request.POST['hiddenInput']
        print(latitude,longitude,val)
        df=getallpos(latitude,longitude)

        print(df)
        gymarray=getgym(df)
        restarray=getrest(df)
        coffeearray=getcoffee(df)
        df["gyms"]=gymarray
        df["restaurants"]=restarray
        df["coffee"]=coffeearray
        shoppingarray=getshopping(df)
        parksarray=getparks(df)
        drinksarray=getdrinks(df)
        df["shopping"]=shoppingarray
        df["parks"]=parksarray
        df["drinks"]=drinksarray
        print(df)
        model = joblib.load('amenity_classifier_py.sav')
        x = df.drop(['latitude','longitude'], axis='columns')
        y = model.predict(x)
        df["cluster"]=y
        print(df)
        user=request.user
        info=people_info.objects.filter(user=user).first()
        user_cluster = info.cluster
        if user_cluster == 2:
            rslt_df=df[(df['cluster']==1)]
        elif user_cluster == 1:
            rslt_df = df[(df['cluster'] == 2)]
        elif user_cluster == 0:
            rslt_df = df[(df['cluster'] == 0)]

        print(rslt_df)
        addr=[]
        lat = rslt_df['latitude'].tolist()
        long= rslt_df['longitude'].tolist()
        print(lat)
        print(long)
        for i in range(len(lat)):
            try:
                strlatlong=str(str(lat[i])+','+str(long[i]))
                location = geolocator.reverse(strlatlong)
                addr.append(location.address)
            except:
                addr.append('Could Not found address')
        print(addr)
        m = folium.Map(location=[latitude, longitude], zoom_start=10)
        for i in range(len(lat)):
            folium.Marker(location=[lat[i], long[i]], tooltip='click for location', popup=str(lat[i]) + ',' +
            str(long[i])).add_to(m)
        m = m._repr_html_()
        points = zip(lat, long, addr)
        context = {'m': m, 'points': points}
        return render(request, 'map.html', context)




    else:
        return HttpResponse("Not Allowed")




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

def logout_view(request):
    logout(request)
    return redirect('Home')


""""@login_required(login_url='/login/')
def map(request):
    lat=[18.548806,17.548810]
    long=[73.870976,74.870970]

    m=folium.Map(location=[18.548806,73.870976],zoom_start=10)
    for i in range(len(lat)):
        folium.Marker(location=[lat[i],long[i]],tooltip='click for location',popup=str(lat[i])+','+str(long[
        i])).add_to(m)
    m=m._repr_html_()
    points=zip(lat,long)
    context={'m':m,'points':points}
    return render(request, 'map.html', context)"""
















import requests
import json


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