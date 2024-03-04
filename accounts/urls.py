from django.urls import path
from . import views
from accounts.views import *

urlpatterns =[
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('profileupdate/',views.user_profileupdate,name='profileupdate'),
    path('changepass/',views.Userchangepassword,name='changepass'),

]