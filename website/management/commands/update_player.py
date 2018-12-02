import requests
import time
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from website.models import Team, Player, Match, UserWatchHistory


TEAM_IN_COMPETITION_BASE_LINK = 'http://api.football-data.org/v2/competitions/{competition_id}/teams'
TEAM_BASE_LINK = 'http://api.football-data.org/v2/teams/{team_id}'


class Command(BaseCommand):
    request_count = 0

    def add_arguments(self, parser):
        parser.add_argument('competition_id', nargs='?', type=int, default=2021)

    def handle(self, *args, **options):
        assert settings.FOOTBALL_API_TOKEN, 'Football API Token is required in environment variable'

        # pause to avoid request limit
        time.sleep(60)

        self.check_and_pause()
        HEADER = {'X-Auth-Token': settings.FOOTBALL_API_TOKEN}
        response = requests.get(
            TEAM_IN_COMPETITION_BASE_LINK.format(competition_id=options['competition_id']),
            headers=HEADER)
        response.raise_for_status()
        json = response.json()

        teams = json['teams']

        for team in teams:
            team_id = team['id']

            self.check_and_pause()
            response = requests.get(TEAM_BASE_LINK.format(team_id=team_id), headers=HEADER)
            response.raise_for_status()
            team_json = response.json()

            team_obj = Team.objects.get(id=team_id)

            squad = team_json['squad']

            for person in squad:
                person_obj, created = Player.objects.get_or_create(
                    id=person['id'],
                    defaults={'name': person['name'], 'nationality': person['nationality'], 'role': person['role']})

                person_obj.team = team_obj
                person_obj.position = person['position']
                person_obj.number = person['shirtNumber']

                person_obj.save()

        self.stdout.write('successfully updated players')

    def check_and_pause(self):
        self.request_count += 1
        if self.request_count >= 10:
            self.stdout.write('Pause for 1 minute')
            time.sleep(60)
            self.stdout.write('Resume')
