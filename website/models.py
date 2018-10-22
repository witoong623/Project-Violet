from django.db import models
from django.contrib.auth import get_user_model


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, default='UNKNOWN')
    display_name = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    POSTPONED = 'POSTPONED'
    SCHEDULED = 'SCHEDULED'
    CANCELED = 'CANCELED'
    SUSPENDED = 'SUSPENDED'
    IN_PLAY = 'IN_PLAY'
    PAUSED = 'PAUSED'
    FINISHED = 'FINISHED'
    AWARDED = 'AWARDED'
    MATCH_STATUS = (
        (POSTPONED, 'Postponed'),
        (SCHEDULED, 'Scheduled'),
        (CANCELED, 'Canceled'),
        (SUSPENDED, 'Suspended'),
        (IN_PLAY, 'In Play'),
        (PAUSED, 'Paused'),
        (FINISHED, 'Finished'),
        (AWARDED, 'Awarded')
    )

    HOME_TEAM = 'HOME_TEAM'
    AWAY_TEAM = 'AWAY_TEAM'
    DRAW = 'DRAW'
    WINNER_TEAM = (
        (HOME_TEAM, 'Home Team'),
        (AWAY_TEAM, 'Away Team'),
        (DRAW, 'Draw')
    )

    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=9, choices=MATCH_STATUS, default=SCHEDULED)
    match_day = models.IntegerField()
    date = models.DateTimeField()

    home_team = models.ForeignKey(Team, models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, models.CASCADE, related_name='away_team')

    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return '{} VS {}'.format(self.home_team, self.away_team)


class UserWatchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'match'),)
