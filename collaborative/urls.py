from django.urls import path

from . import views

app_name = 'collaborative'
urlpatterns = [
    path('', views.index, name='index'),
    path('simulatesimilaruser/', views.simulate_fiding_similar_users, name='simulate_finding_knn'),
    path('jaccardsimulatesimilaruser/', views.simulate_jaccard, name='simulate_finding_jaccard'),
    path('jaccardsimulatesimilaruser2/', views.simulate_jaccard2, name='simulate_finding_jaccard2'),
]