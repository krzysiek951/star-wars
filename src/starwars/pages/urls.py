from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/<str:collection_id>', views.collection_details, name='collection'),
    path('swapi_custom_fetch/<str:resource>', views.swapi_custom_fetch, name='swapi_custom_fetch'),
    path('swapi_default_fetch/<str:resource>', views.swapi_default_fetch, name='swapi_default_fetch'),
    path('tripaway_default_fetch/<str:resource>', views.tripaway_default_fetch, name='tripaway_default_fetch'),
]
