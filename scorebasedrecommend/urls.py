from django.urls import path
from . import views

app_name = 'scorebasedrecommend'
urlpatterns = [
    path('', views.index, name='index'),
    path('score-table/', views.score_table, name='score_table'),
    path('recommended-teams/', views.recommended_teams, name='recommended_teams'),
    path('recommended-matches/', views.recommended_matches, name='recommended_matches'),
]
