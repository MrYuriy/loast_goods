#from django.conf.urls import url
from django.urls import path, include 
from .views import GenadresView

urlpatterns = [
    path('api/', GenadresView.as_view()),
]
