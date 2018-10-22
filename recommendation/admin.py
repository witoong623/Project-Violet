from django.contrib import admin
from django.db.models import Q
from .models import MatchSchedule
from .models import League
from .models import UserWatch
from .models import Round
from .models import Team
from .models import Player
from .models import MatchProfileValues
from .models import UserWatchGenerateQueries


class UserCaseListFilter(admin.SimpleListFilter):
    title = ('user case')
    parameter_name = 'user_case'

    def lookups(self, request, model_admin):
        return [
            ('u1', ('U1: Man U')),
            ('u11', ('U11: Man U and Arsenal')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'u1':
            return queryset.filter(Q(ms_team1=19) | Q(ms_team2=19))

        if self.value() == 'u11':
            return queryset.filter(Q(ms_team1=19) | Q(ms_team2=19) | Q(ms_team1=1) | Q(ms_team2=1))


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'active_flag')
    list_filter = ('active_flag', 't_id')
    actions = ['set_inactive', 'set_active']

    def set_inactive(self, request, queryset):
        queryset.update(active_flag=False)
    set_inactive.short_description = 'Set inactive'

    def set_active(self, request, queryset):
        queryset.update(active_flag=True)
    set_active.short_description = 'Set active'


class UserWatchGenerateQueriesAdmin(admin.ModelAdmin):
    list_display = ('uwg_id', 'uwg_description')


class MatchScheduleAdmin(admin.ModelAdmin):
    list_display = ('ms_id', 'ms_team1', 'ms_team2', 'ms_time')
    list_filter = (UserCaseListFilter, 'ms_league', 'ms_season')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team)
admin.site.register(Round)
admin.site.register(MatchSchedule, MatchScheduleAdmin)
admin.site.register(League)
admin.site.register(UserWatch)
admin.site.register(MatchProfileValues)
admin.site.register(UserWatchGenerateQueries, UserWatchGenerateQueriesAdmin)
