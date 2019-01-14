from django.contrib import admin
from .models import RecommendedMatch


class RecommendedMatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'recommendatoin_type', 'value')
    list_filter = ('recommendatoin_type', 'user')

admin.site.register(RecommendedMatch, RecommendedMatchAdmin)
