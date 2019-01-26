import sys
from django.test import TestCase
from django.utils import timezone
from core.recommendation.common import get_competition_table
from website.models import Competition


class ScoreTableTestCase(TestCase):
    fixtures = ['websitefixture.json']

    def test_no_exception(self):
        premier_league = Competition.objects.get(id=2021)
        table = get_competition_table(premier_league, timezone.now())
