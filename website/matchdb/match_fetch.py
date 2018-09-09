import requests
import json
import dateutil.parser
from django.conf import settings
from ..models import Team, Match

PL_2018_LINK = 'http://api.football-data.org/v2/competitions/2021/matches?season=2018'

def fetch_and_update_match():
    assert settings.FOOTBALL_API_TOKEN, 'Football API Token is required in environment variable'

    HEADER = { 'X-Auth-Token': settings.FOOTBALL_API_TOKEN }
    response = requests.get(PL_2018_LINK, headers=HEADER)
    response.raise_for_status()
    json = response.json()

    matches = json['matches']

    for json_match in matches:
        id = json_match['id']

        try:
            match = Match.objects.get(id=id)
            match.status = json_match['status']
            match.save()
            continue
        except Match.DoesNotExist:
            pass

        status = json_match['status']
        match_day = json_match['matchday']
        date = dateutil.parser.parse(json_match['utcDate'])

        match = Match(id=id, status=status, match_day=match_day, date=date)

        home_team_json = json_match['homeTeam']
        away_team_json = json_match['awayTeam']

        match.home_team = Team.objects.get_or_create(id=home_team_json['id'], defaults={'name': home_team_json['name']})[0]
        match.away_team = Team.objects.get_or_create(id=away_team_json['id'], defaults={'name': away_team_json['name']})[0]

        match.save()
