from django.urls import path

from . import views

app_name = 'recommendation'
urlpatterns = [
    path('', views.index, name='index'),
    path('getrecommend/', views.getrecommend, name='getrecommend'),
    path('results/<str:user_id>/<str:until>/', views.results, name='results'),
    path('results/<str:user_id>/', views.results, name='results'),
    path('preference-table/', views.preference_table, name='preference_table')
]