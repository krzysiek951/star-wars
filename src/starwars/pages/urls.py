from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/<str:collection_id>', views.collection_details, name='collection'),
    path('fetch_starwars_people/', views.fetch_starwars_people, name='fetch_starwars_people'),
]
