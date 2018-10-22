import os
from datetime import timedelta, datetime, timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Match


def index(request):
    # today matches
    # from this momemt until next 24 hours
    today_min = timezone.now()
    today_max = today_min + timedelta(days=1)
    today_matches_query = Match.objects.filter(date__range=(today_min, today_max))

    today_matches = []

    for match in today_matches_query:
        entry = {
            'home_team': match.home_team.display_name,
            'away_team': match.away_team.display_name,
            'home_logo': match.home_team.short_name,
            'away_logo': match.away_team.short_name,
            'date': match.date
        }

        today_matches.append(entry)

    # last 4 matches with score
    now = timezone.now()
    previous_matches_query = Match.objects.filter(date__lt=now).order_by('-date')[:4]

    previous_matches = []

    for match in previous_matches_query:
        entry = {
            'home_team': match.home_team.display_name,
            'away_team': match.away_team.display_name,
            'home_logo': match.home_team.short_name,
            'away_logo': match.away_team.short_name,
            'date': match.date,
            'home_score': match.home_score,
            'away_score': match.away_score
        }

        previous_matches.append(entry)

    # upcomming matches: matches that are not today matches but next matches in row
    last_previous_match = previous_matches_query.first()
    upcomming_matches = []

    if last_previous_match is not None:
        last_match_day = last_previous_match.match_day
        upcomming_matches_query = Match.objects.filter(match_day=last_match_day + 1).order_by('date')

        for match in upcomming_matches_query:
            entry = {
                'home_team': match.home_team.display_name,
                'away_team': match.away_team.display_name,
                'home_logo': match.home_team.short_name,
                'away_logo': match.away_team.short_name,
                'date': match.date
            }

            upcomming_matches.append(entry)

    context = {
        'today_matches': today_matches,
        'previous_matches': previous_matches,
        'upcomming_matches': upcomming_matches
    }

    return render(request, 'website/index.html', context=context)


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
