from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, default='UNKNOWN')
    display_name = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name


class MatchManager(models.Manager):
    manchester_derby = None
    merseyside_derby = None
    north_london_derby = None
    north_west_derby = None

    def derby_matches(self, after=timezone.now()):
        # find all derby teams first
        if self.manchester_derby is None:
            self.manchester_derby = Team.objects.filter(Q(id=65) | Q(id=66))

        if self.merseyside_derby is None:
            self.merseyside_derby = Team.objects.filter(Q(id=62) | Q(id=64))

        if self.north_london_derby is None:
            self.north_london_derby = Team.objects.filter(Q(id=57) | Q(id=73))

        if self.north_west_derby is None:
            self.north_west_derby = Team.objects.filter(Q(id=66) | Q(id=64))

        # find matches that both team in derby teams compete
        qs = (self
              .filter(date__gt=after)
              .filter(
                     (Q(home_team__in=self.manchester_derby) & Q(away_team__in=self.manchester_derby)) |
                     (Q(home_team__in=self.merseyside_derby) & Q(away_team__in=self.merseyside_derby)) |
                     (Q(home_team__in=self.north_london_derby) & Q(away_team__in=self.north_london_derby)) |
                     (Q(home_team__in=self.north_west_derby) & Q(away_team__in=self.north_west_derby))
              )
              .select_related('home_team', 'away_team'))
        return qs


class Match(models.Model):
    objects = MatchManager()

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

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')

    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=9, blank=True)

    competition = models.ForeignKey('Competition', related_name='matches', on_delete=models.CASCADE)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)

    def __str__(self):
        return '{} VS {}'.format(self.home_team, self.away_team)


class UserWatchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_watches')
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'match'),)


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    currentSeason = models.ForeignKey('Season', blank=True, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Season(models.Model):
    id = models.IntegerField(primary_key=True)
    startDate = models.DateField()
    endDate = models.DateField()
    currentMatchday = models.IntegerField()
    display_name = models.CharField(max_length=20, blank=True)

    teams = models.ManyToManyField(Team)
    winner = models.ForeignKey(Match, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    competition = models.ForeignKey(Competition, related_name='seasons', on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name


class Player(models.Model):
    GOALKEEPER = 'Goalkeeper'
    DEFENDER = 'Defender'
    MIDFIELDER = 'Midfielder'
    ATTACKER = 'Attacker'
    POSITIONS = (
        (GOALKEEPER, 'Goalkeeper'),
        (DEFENDER, 'Defender'),
        (MIDFIELDER, 'Midfielder'),
        (ATTACKER, 'Attacker')
    )

    PLAYER = 'PLAYER'
    COACH = 'COACH'
    ASSISTANT_COACH = 'ASSISTANT_COACH'
    ROLES = (
        (PLAYER, 'Player'),
        (COACH, 'Coach'),
        (ASSISTANT_COACH, 'Assistant Coach')
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    nationality = models.CharField(max_length=30)
    number = models.IntegerField(null=True, blank=True)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='players', null=True, blank=True)
    position = models.CharField(max_length=10, choices=POSITIONS, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLES)

    influence = models.BooleanField(default=False)

    def __str__(self):
        return self.name
