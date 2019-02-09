from django.contrib import admin
from django.db.models import Q
from .models import Match, Team, Player, UserWatchHistory, Season, Competition


class MatchContainTeam(admin.SimpleListFilter):
    title = 'Contain team'
    parameter_name = 'team_id'

    def lookups(self, request, model_admin):
        return [(team.id, team.display_name) for team in Team.objects.all()] + [('all', ('All Teams'))]

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset.all()
        else:
            return queryset.filter(Q(home_team=self.value()) | Q(away_team=self.value()))


class MatchAdmin(admin.ModelAdmin):
    list_display = ('its_name', 'competition', 'season')
    list_filter = (MatchContainTeam,)

    def its_name(self, obj):
        return obj.__str__()


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'short_name')


class UserWatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'match')


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_season')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'competition')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    list_filter = ('team',)


admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserWatchHistory, UserWatchHistoryAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Player, PlayerAdmin)
