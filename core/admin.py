from django.contrib import admin
from .models import RecommendedMatch


class RecommendedMatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'recommendatoin_type')
    list_filter = ('recommendatoin_type',)

admin.site.register(RecommendedMatch, RecommendedMatchAdmin)
