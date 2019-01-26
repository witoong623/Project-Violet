from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.models import ScoreTable
from core.recommendation.common import get_competition_table
from website.models import Competition


class Command(BaseCommand):
    help = 'Generate recommended matches for every user and store in DB'

    def handle(self, *args, **options):
        premier_league = Competition.objects.get(id=2021)
        season = premier_league.current_season
        scoretable = get_competition_table(premier_league, timezone.now())

        for i, row in enumerate(scoretable.score_table, 1):
            ScoreTable.objects.update_or_create(
                competition=premier_league,
                season=season,
                team=row.team,
                defaults={'played': row.played, 'rank': i, 'won': row.won, 'draw': row.drawn, 'lost': row.lost, 'point': row.point}
            )

        self.stdout.write('Complete generate score table')
