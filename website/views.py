import os
from datetime import timedelta, datetime, timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q
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
    team = get_object_or_404(Team, id=team_id)

    context = {
        'team': team,
        'players': team.players.order_by('number')
    }

    return render(request, 'website/team-standing.html', context=context)
