from django.test import TestCase
from .website_fake_data import MatchFactory
from website.models import Match
from ..recommendation.contentbased import get_match_profile, MatchProfile


class UserProfileTests(TestCase):
    def setUp(self):
        match = MatchFactory(id=623, home_team__id=19, away_team__id=20)

    def test_generate_data(self):
        '''
        This test is for try to generating data using factory boy only.
        '''
        match = Match.objects.get(id=623)

        self.assertEqual(match.home_team.id, 19)
        self.assertEqual(match.away_team.id, 20)

    def test_get_user_profile(self):
        pass


class MatchProfileTest(TestCase):
    def setUp(self):
        # default match setting is on SAT
        match = MatchFactory(id=623, home_team__id=19, away_team__id=20)

    def test_get_match_profile(self):
        match_profile = get_match_profile(623)

        actual_match_profile = MatchProfile(623)
        actual_match_profile.competitionmatrix = 1
        actual_match_profile.teamsmatrix = (19, 20)
        actual_match_profile.timematrix = 2

        self.assertEqual(match_profile.id, actual_match_profile.id)
        self.assertEqual(match_profile.competitionmatrix, actual_match_profile.competitionmatrix)
        self.assertTupleEqual(match_profile.teamsmatrix, actual_match_profile.teamsmatrix)
        self.assertEqual(match_profile.timematrix, actual_match_profile.timematrix)
