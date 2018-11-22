from django.contrib import admin
from .models import Match, Team, Player, UserWatchHistory, Season, Competition


class MatchAdmin(admin.ModelAdmin):
    list_display = ('its_name', 'competition', 'season')

    def its_name(self, obj):
        return obj.__str__()


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'short_name')


class UserWatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'match')


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'currentSeason')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'competition')


admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserWatchHistory, UserWatchHistoryAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Player)
