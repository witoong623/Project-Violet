import os
from datetime import timedelta, datetime, timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from .models import Match


COMPETITION = ['pl', 'bl1', 'pd']
COMPETITION_ID = {
    'pl': 2021
}


def index(request):
    return render(request, 'website/index.html')


def get_comming_matches(request):
    # last 4 matches with score
    now = timezone.now()
    last_previous_match = Match.objects.filter(date__lt=now).order_by('-date').first()
    upcomming_matches = []

    last_match_day = last_previous_match.match_day
    upcomming_matches_query = Match.objects.filter(match_day=last_match_day + 1).order_by('date')

    for match in upcomming_matches_query:
        entry = {
            'id': match.id,
            'home_team': match.home_team.display_name,
            'away_team': match.away_team.display_name,
            'home_logo': os.path.join(settings.STATIC_URL, 'website/images/', '{}.png'.format(match.home_team.short_name)),
            'away_logo': os.path.join(settings.STATIC_URL, 'website/images/', '{}.png'.format(match.away_team.short_name)),
            'date': match.date
        }

        upcomming_matches.append(entry)

    return JsonResponse(upcomming_matches, safe=False)


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
