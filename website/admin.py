from django.contrib import admin
from .models import Match, Team, UserWatchHistory


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'short_name')


class UserWatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'match')


admin.site.register(Match)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserWatchHistory, UserWatchHistoryAdmin)
