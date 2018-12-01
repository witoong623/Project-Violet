import os
from django.conf import settings
from rest_framework import serializers
from ..models import Match, UserWatchHistory


class MatchSerialzer(serializers.ModelSerializer):
    home_logo = serializers.SerializerMethodField()
    away_logo = serializers.SerializerMethodField()
    home_team = serializers.CharField(source='home_team.display_name')
    away_team = serializers.CharField(source='away_team.display_name')

    def get_home_logo(self, obj):
        return os.path.join(settings.STATIC_URL, 'website/images/', '{}.png'.format(obj.home_team.name))

    def get_away_logo(self, obj):
        return os.path.join(settings.STATIC_URL, 'website/images/', '{}.png'.format(obj.away_team.name))

    class Meta:
        model = Match
        fields = ('id',
                  'home_team',
                  'away_team',
                  'date',
                  'home_logo',
                  'away_logo',
                  'home_score',
                  'away_score')


class UserWatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # matchId = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all(), source='match')

    class Meta:
        model = UserWatchHistory
        fields = ('id', 'match', 'user')
        validators = [
            serializers.UniqueTogetherValidator(
                UserWatchHistory.objects.all(),
                ('user', 'match')
            )
        ]
