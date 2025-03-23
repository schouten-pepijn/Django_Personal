from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('cached_hello/', views.cached_hello),
    path('cached_hello_2/', views.cached_hello_2)
]
