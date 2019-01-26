from django.contrib import admin
from .models import RecommendedMatch, ScoreTable


class RecommendedMatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'recommendatoin_type', 'value')
    list_filter = ('recommendatoin_type', 'user')


class ScoreTableAdmin(admin.ModelAdmin):
    list_display = ('rank', 'competition', 'season', 'team', 'won', 'draw', 'lost')
    list_filter = ('competition', 'season')


admin.site.register(RecommendedMatch, RecommendedMatchAdmin)
admin.site.register(ScoreTable, ScoreTableAdmin)
