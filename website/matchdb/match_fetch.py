import requests
import json
import dateutil.parser
from django.conf import settings
from ..models import Team, Match

PL_2018_LINK = 'http://api.football-data.org/v2/competitions/2021/matches?season=2018'


# use 'python manage.py runcrons --force' to force run this cron
def fetch_and_update_match():
    assert settings.FOOTBALL_API_TOKEN, 'Football API Token is required in environment variable'

    HEADER = {'X-Auth-Token': settings.FOOTBALL_API_TOKEN}
    response = requests.get(PL_2018_LINK, headers=HEADER)
    response.raise_for_status()
    json = response.json()

    matches = json['matches']

    for json_match in matches:
        id = json_match['id']

        try:
            match = Match.objects.get(id=id)
            status = json_match['status']

            if status == Match.FINISHED:
                match.status = status
                score_node = json_match['score']
                match.winner = score_node['winner']
                match.home_score = score_node['fullTime']['homeTeam']
                match.away_score = score_node['fullTime']['awayTeam']
                match.save()

            continue
        except Match.DoesNotExist:
            # this mean that current match haven't been added to DB before
            pass

        status = json_match['status']
        match_day = json_match['matchday']
        date = dateutil.parser.parse(json_match['utcDate'])

        match = Match(id=id, status=status, match_day=match_day, date=date)

        if status == Match.FINISHED:
            score_node = json_match['score']
            match.winner = score_node['winner']
            match.home_score = score_node['fullTime']['homeTeam']
            match.away_score = score_node['fullTime']['awayTeam']

        home_team_json = json_match['homeTeam']
        away_team_json = json_match['awayTeam']

        match.home_team = Team.objects.get_or_create(id=home_team_json['id'], defaults={'name': home_team_json['name']})[0]
        match.away_team = Team.objects.get_or_create(id=away_team_json['id'], defaults={'name': away_team_json['name']})[0]

        match.save()
