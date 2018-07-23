from django.urls import path
from . import views

app_name = 'cosinesimulation'
urlpatterns = [
    path('', views.index, name='index'),
    path('simulation_data/', views.simulation_data, name='simulationdata'),
    path('simulate/', views.simulate, name='simulate'),
]