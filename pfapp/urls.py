from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path("", views.index,name="Home"),
path("signup/",views.signup,name="signup"),
path("handle_signup/",views.handle_signup,name="handle_signup"),
path("login/",views.loginpage,name="login"),
path("handle_login/",views.handle_login,name="handle_login"),
path("homepage/",views.homepage,name="homepage"),
path("handle_user_info/",views.handle_user_info,name="handle_user_info"),
path("handle_input_name/",views.handle_input_name,name="handle_input_name"),
path("handle_latlong/",views.handle_latlong,name="handle_latlong"),
path("logout_view/",views.logout_view,name="logout_view"),


]