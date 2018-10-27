import datetime
import factory
from factory.fuzzy import FuzzyInteger
from website.models import Team, Competition, Season, Match


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    id = FuzzyInteger(10, 100)
    name = factory.Faker('name')


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition
        django_get_or_create = ('id',)

    id = 1
    name = 'Fake competition'
    code = 'FC'


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Season

    id = 1
    startDate = datetime.date(2018, 1, 1)
    endDate = datetime.date(2019, 1, 1)
    currentMatchday = 1

    competition = factory.SubFactory(CompetitionFactory)


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Match

    id = 1
    status = Match.FINISHED
    match_day = 1
    date = datetime.datetime(2018, 10, 20)

    home_team = factory.SubFactory(TeamFactory)
    away_team = factory.SubFactory(TeamFactory)

    competition = factory.SubFactory(CompetitionFactory)
    season = factory.SubFactory(SeasonFactory)
