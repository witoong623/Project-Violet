import os
from datetime import timedelta, datetime, timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q

from core.models import ScoreTable
from .models import Match, Team, Competition


COMPETITION = ['pl', 'bl1', 'pd']
COMPETITION_ID = {
    'pl': 2021
}


def index(request):
    return render(request, 'website/index.html')


def competition_view(request, name):
    title = None

    if name == 'pl':
        title = 'Premier League'
    elif name == 'bl1':
        title = 'Bundesliga'
    elif name == 'pd':
        title = 'Laliga'
    else:
        return Http404()

    context = {
        'title': title,
        'competition_id': COMPETITION_ID[name]
    }

    return render(request, 'website/competition.html', context=context)


def standing_list_view(request, name):
    if name == 'pl':
        premier_league = Competition.objects.get(code='PL')

        context = {
            'teams': premier_league.current_season.teams.all(),
            'title': 'Premier League Season {}'.format(premier_league.current_season.display_name)
        }

        return render(request, 'website/standing-list.html', context=context)
    else:
        return Http404()


def team_standing(request, team_id):
    premier_league = Competition.objects.get(id=2021)
    season = premier_league.current_season
    team = get_object_or_404(Team, id=team_id)
    score_table = ScoreTable.objects.filter(team=team, competition=premier_league, season=season).first()

    context = {
        'team': team,
        'players': team.players.exclude(Q(role='PLAYER') & Q(number=None)).order_by('number'),
        'stat': score_table
    }

    return render(request, 'website/team-standing.html', context=context)


def table_view(request, name):
    title = None

    if name == 'pl':
        title = 'Premier League'
    elif name == 'bl1':
        title = 'Bundesliga'
    elif name == 'pd':
        title = 'Laliga'
    else:
        return Http404()

    competition = Competition.objects.get(pk=COMPETITION_ID[name])
    score_table = ScoreTable.objects.filter(competition=competition, season=competition.current_season).select_related('team')

    context = {
        'title': title,
        'score_table': score_table
    }

    return render(request, 'website/table.html', context=context)
