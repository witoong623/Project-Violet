import datetime
from jaccardcollaborative import jaccard
from django.test import TestCase
from recommendation.models import MatchSchedule
from django.db.models import Q


class JaccardCollaborativeModuleTest(TestCase):
    fixtures = ['football.json']
    MAN_U_ID = 19
    ARSENAL_ID = 1

    def test_identify_like_teams_entire_season_one_team(self):
        after_last_match = datetime.datetime(2018, 5, 14).astimezone()

        all_man_u = MatchSchedule.objects.filter(Q(ms_league_id=1) & Q(ms_time__lt=after_last_match)).filter(Q(ms_team1=self.MAN_U_ID) | Q(ms_team2=self.MAN_U_ID))
        all_man_u_ids = [m.ms_id for m in all_man_u]

        like_teams = jaccard.identify_like_teams(all_man_u_ids, until=after_last_match)

        # watch all matches is definitely more than 80%
        self.assertListEqual(like_teams, [self.MAN_U_ID])

    def test_identify_like_teams_entire_season_two_team(self):
        after_last_match = datetime.datetime(2018, 5, 14).astimezone()

        all_man_u_arsenal = MatchSchedule.objects.filter(Q(ms_league_id=1) & Q(ms_time__lt=after_last_match)).filter(Q(ms_team1=self.MAN_U_ID) | Q(ms_team2=self.MAN_U_ID) | Q(ms_team1=self.ARSENAL_ID) | Q(ms_team2=self.ARSENAL_ID))
        ids = [m.ms_id for m in all_man_u_arsenal]

        like_teams = jaccard.identify_like_teams(ids, until=after_last_match)

        self.assertListEqual(like_teams, [self.ARSENAL_ID, self.MAN_U_ID])

    def test_identify_teams_id_with_matches_id_one_team(self):
        after_last_match = datetime.datetime(2018, 5, 14).astimezone()

        all_man_u = MatchSchedule.objects.filter(Q(ms_league_id=1) & Q(ms_time__lt=after_last_match)).filter(Q(ms_team1=self.MAN_U_ID) | Q(ms_team2=self.MAN_U_ID))
        all_man_u_ids = [m.ms_id for m in all_man_u]

        teams_matches_dict = jaccard.identify_teams_id_with_matches_id(all_man_u_ids, after_last_match)

        self.assertSetEqual(set(teams_matches_dict[self.MAN_U_ID]), set(all_man_u_ids))

    def test_identify_teams_id_with_matches_id_two_team(self):
        after_last_match = datetime.datetime(2018, 5, 14).astimezone()

        all_man_u = MatchSchedule.objects.filter(Q(ms_league_id=1) & Q(ms_time__lt=after_last_match)).filter(Q(ms_team1=self.MAN_U_ID) | Q(ms_team2=self.MAN_U_ID))
        all_man_u_ids = [m.ms_id for m in all_man_u]

        all_arsenal = MatchSchedule.objects.filter(Q(ms_league_id=1) & Q(ms_time__lt=after_last_match)).filter(Q(ms_team1=self.ARSENAL_ID) | Q(ms_team2=self.ARSENAL_ID))
        all_arsenal_ids = [m.ms_id for m in all_arsenal]

        teams_matches_dict = jaccard.identify_teams_id_with_matches_id(list(set().union(all_man_u_ids, all_arsenal_ids)), after_last_match)

        self.assertSetEqual(set(teams_matches_dict[self.MAN_U_ID]), set(all_man_u_ids))
        self.assertSetEqual(set(teams_matches_dict[self.ARSENAL_ID]), set(all_arsenal_ids))
