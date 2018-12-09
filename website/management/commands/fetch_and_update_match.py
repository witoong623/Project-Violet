import requests
import json
import dateutil.parser
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from website.models import Team, Match, Competition, Season


PL_2018_LINK = 'http://api.football-data.org/v2/competitions/2021/matches?season=2018'
COMPETITION_DETAIL_BASE_LINK = 'http://api.football-data.org/v2/competitions/'


class Command(BaseCommand):
    display_names = settings.TEAMS_DISPLAY_NAME

    def handle(self, *args, **options):
        assert settings.FOOTBALL_API_TOKEN, 'Football API Token is required in environment variable'

        HEADER = {'X-Auth-Token': settings.FOOTBALL_API_TOKEN}
        response = requests.get(PL_2018_LINK, headers=HEADER)
        response.raise_for_status()
        json = response.json()

        matches = json['matches']

        competition, season = self.fetch_and_update_competition_and_season(json)

        for json_match in matches:
            id = json_match['id']

            try:
                match = Match.objects.get(id=id)
                status = json_match['status']

                if status == Match.FINISHED:
                    match.status = status
                    score_node = json_match['score']
                    match.winner = score_node['winner']
                    match.home_half_score = score_node['halfTime']['homeTeam']
                    match.away_half_score = score_node['halfTime']['awayTeam']
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

            match = Match(id=id, status=status, match_day=match_day, date=date, competition=competition, season=season)

            if status == Match.FINISHED:
                score_node = json_match['score']
                match.winner = score_node['winner']
                match.home_half_score = score_node['halfTime']['homeTeam']
                match.away_half_score = score_node['halfTime']['awayTeam']
                match.home_score = score_node['fullTime']['homeTeam']
                match.away_score = score_node['fullTime']['awayTeam']

            home_team_json = json_match['homeTeam']
            away_team_json = json_match['awayTeam']

            match.home_team = Team.objects.get_or_create(
                id=home_team_json['id'], defaults={'name': home_team_json['name'], 'display_name': self.display_names[home_team_json['id']]})[0]
            match.away_team = Team.objects.get_or_create(
                id=away_team_json['id'], defaults={'name': away_team_json['name'], 'display_name': self.display_names[away_team_json['id']]})[0]

            match.save()

        self.stdout.write('Successfully update {}'.format(len(matches)))

    def fetch_and_update_competition_and_season(self, match_json):
        '''Get JSON represents current competition from competitions/<int:id>/matches?season=<int:year>
           and return Competition and Season of current competition '''
        competition_node = match_json['competition']
        compet_id = competition_node['id']
        competition, competition_created = Competition.objects.get_or_create(
            id=compet_id,
            defaults={
                'name': competition_node['name'],
                'code': competition_node['code']
            }
        )

        assert settings.FOOTBALL_API_TOKEN, 'Football API Token is required in environment variable'

        HEADER = {'X-Auth-Token': settings.FOOTBALL_API_TOKEN}
        response = requests.get(
            COMPETITION_DETAIL_BASE_LINK + str(compet_id), headers=HEADER)
        response.raise_for_status()
        compet_json = response.json()

        current_season_node = compet_json['currentSeason']
        season, season_created = Season.objects.get_or_create(
            id=current_season_node['id'],
            defaults={
                'startDate': dateutil.parser.parse(current_season_node['startDate']).date(),
                'endDate': dateutil.parser.parse(current_season_node['endDate']).date(),
                'currentMatchday': current_season_node['currentMatchday'],
                'competition': competition
            }
        )

        if not season_created:
            season.currentMatchday = current_season_node['currentMatchday']
            season.save()

        if competition_created:
            competition.current_season = season
            competition.save()

        return (competition, season)
