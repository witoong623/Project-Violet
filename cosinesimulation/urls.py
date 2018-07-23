from django.urls import path
from . import views

app_name = 'cosinesimulation'
urlpatterns = [
    path('', views.index, name='index'),
    path('simulation_data/', views.simulation_data, name='simulationdata'),
    path('simulate/', views.simulate, name='simulate'),
    path('onefavorite/<str:afterTime>/', views.onefavorite, name='onefavorite'),
    path('onefavorite_extra/', views.onefavorite_extra, name='onefavoriteextra'),
    path('twofavorite_extra/', views.twofavorite_extra, name='twofavoriteextra'),
    path('onefavorite_extra_afc/', views.onefavorite_extra_afc, name='onefavoriteextra'),
]