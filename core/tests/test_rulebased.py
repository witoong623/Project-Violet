import sys
from django.test import TestCase
from django.utils import timezone
from core.recommendation.rulebased import get_recommended_teams, get_recommended_matches
from website.models import Competition


class TeamRecommendTestCase(TestCase):
    fixtures = ['websitefixture.json']

    def test_no_exception(self):
        premier_league = Competition.objects.get(id=2021)
        recommended_teams = get_recommended_teams(premier_league, timezone.now())
        recommended_teams = get_recommended_teams(premier_league, timezone.now(), cal_at=23)


class RulebasedMatchRecommendTestCase(TestCase):
    fixtures = ['websitefixture.json']

    def test_no_exception(self):
        premier_league = Competition.objects.get(id=2021)
        recommended_matches = get_recommended_matches(premier_league, timezone.now(), 23)
