from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/<str:collection_id>', views.collection_details, name='collection'),
    path('fetch/<str:api>/<str:resource>', views.fetch, name='fetch'),
]
