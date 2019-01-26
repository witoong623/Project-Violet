from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .api import views as api_views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='website/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='website:index'), name='logout'),

    path('competition/<str:name>/', views.competition_view, name='competition'),
    # /standing-list/<name>/
    path('standing-list/<str:name>/', views.standing_list_view, name='standing_list'),
    # /standing/<team_id>/
    path('standing/<int:team_id>/', views.team_standing, name='team_standing'),

    # /today-matches/
    path('today-matches/', api_views.TodayMatchesList.as_view(), name='today_matches'),
    # /upcomming-matches/
    path('upcomming-matches/', api_views.UpcommingMatchesList.as_view(), name='upcomming_matches'),
    # /recent-match/
    path('recent-matches/', api_views.RecentMatchesList.as_view(), name='recent_matches'),
    # /userwatchhistory/
    path('userwatchhistory/', api_views.UserWatchHistoryListCreateDestroyAPIView.as_view(), name='userwatchhistory'),
    # /userwatchhistory/:pk/
    path('userwatchhistory/<int:pk>/', api_views.UserWatchHistoryListCreateDestroyAPIView.as_view(), name='userwatchhistory'),
    # /recommended-matches/
    path('recommended-matches/', api_views.RecommendedMatchesList.as_view(), name='recommended_matches'),
    # /competition/:pk/
    path('api/competition/<int:competition>/', api_views.CompetitionMatchesList.as_view(), name='competition_matches'),
    # /table/<str:name>/
    path('table/<str:name>/', views.table_view, name='table'),
]
