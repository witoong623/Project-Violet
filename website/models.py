from django.db import models

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
    WINNER_TEAM = (
        (HOME_TEAM, 'Home Team'),
        (AWAY_TEAM, 'Away Team')
    )

    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=9, choices=MATCH_STATUS, default=SCHEDULED)
    match_day = models.IntegerField()
    date = models.DateTimeField()

    home_team = models.ForeignKey(Team, models.CASCADE)
    away_team = models.ForeignKey(Team, models.CASCADE)
    

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

