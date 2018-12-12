from datetime import datetime
from typing import List, Dict, Sequence
from django.utils import timezone
from django.db.models import Q
from core.recommendation.common import get_competition_table, CompetitionTable
from website.models import Competition, Team, Match


class RecommendedTeam:
    def __init__(self, team: Team, point: float):
        self.team = team
        self.point = point


class RecommendedResult:
    TOP_TEAMS = '1st and 2nd in table'
    ALMOST_RELEGATED_TEAMS = 'Almost get relegated teams'
    DERBY_MATCHES = 'Derby matches'
    WINNER_DECIDE_MATCHES = 'Winner decide matches'
    RELEGATION_DECIDE_MATCHES = 'Relegation decide matches'

    point: float = 0
    recommend_methods: str = ''

    def add_recommend_method(self, method: str):
        if self.recommend_methods != '':
            self.recommend_methods += ', ' + method
        else:
            self.recommend_methods += method

    def __init__(self, match: Match):
        self.match = match


class RuleBasedRecommendationEngine:
    cal_at: int
    __competitiontable_cache: CompetitionTable = None

    def __init__(self, competition: Competition, at_date=timezone.now(), cal_at=10):
        self.competition = competition
        self.at_date = at_date
        self.cal_at = cal_at

    def __get_competitiontable_cache(self):
        if self.__competitiontable_cache is None:
            self.__competitiontable_cache = get_competition_table(self.competition, self.at_date)
        return self.__competitiontable_cache

    def __get_derby_matches(self):
        return Match.objects.derby_matches(self.at_date).select_related('home_team', 'away_team').all()

    def __get_top_teams_matches(self):
        competition_table = self.__get_competitiontable_cache()

        # top teams is 1st and 2nd
        top_teams = [row.team for row in competition_table.score_table[0:2]]
        top_teams_matches = (Match
                             .objects
                             .filter(date__gt=self.at_date)
                             .filter(Q(home_team__in=top_teams) | Q(away_team__in=top_teams))
                             .select_related('home_team', 'away_team')
                             .all())

        return top_teams_matches

    def __get_almost_relegated_teams_matches(self):
        competition_table = self.__get_competitiontable_cache()

        # 17th and 18th place
        low_teams = [row.team for row in competition_table.score_table[16:18]]
        low_teams_matches = (Match
                             .objects
                             .filter(date__gt=self.at_date)
                             .filter(Q(home_team__in=low_teams) | Q(away_team__in=low_teams))
                             .select_related('home_team', 'away_team')
                             .all())

        return low_teams_matches

    def __get_winner_decide_matches(self):
        competition_table = self.__get_competitiontable_cache()

        # winner candidate are 1st and 2nd place
        fp = competition_table.score_table[0]
        sp = competition_table.score_table[1]

        if fp.get_remaining_matches_count() <= 2 & sp.get_remaining_matches_count() <= 2:
            if fp.point + fp.get_remaining_matches_count() * 3 > sp.point:
                return fp.team.get_remaining_matches(self.at_date)
            elif sp.point + sp.get_remaining_matches_count() * 3 > fp.point:
                return sp.team.get_remaining_matches(self.at_date)
            else:
                return fp.team.get_remaining_matches(self.at_date).union(
                    sp.team.get_remaining_matches(self.at_date)
                )
        else:
            # case remaining matches more than 2
            first_next_2_matches_point = fp.point + 6

            if first_next_2_matches_point > sp.get_best_point():
                # case if 1st win next 2 matches is guaranteed to be a winner
                return fp.team.next_n_matches(self.at_date, n=2)
            else:
                return Match.objects.none()

    def __get_relegattion_decide_matches(self):
        competition_table = self.__get_competitiontable_cache()

        # relegation candidate are 17th, 18th
        seven = competition_table.score_table[16]
        eight = competition_table.score_table[17]

        if seven.get_remaining_matches_count() <= 2 & eight.get_remaining_matches_count() <= 2:
            if seven.point + seven.get_remaining_matches_count() * 3 > eight.point:
                return seven.team.get_remaining_matches(self.at_date)
            elif eight.point + eight.get_remaining_matches_count() * 3 > seven.point:
                return eight.team.get_remaining_matches(self.at_date)
            else:
                return seven.team.get_remaining_matches(self.at_date).union(
                    eight.team.get_remaining_matches(self.at_date)
                )
        else:
            # case remaining matches more than 2
            seven_next_2_matches_point = seven.point + 6

            if seven_next_2_matches_point > eight.get_best_point():
                # case guarantee to not be relegated
                return seven.team.next_n_matches(self.at_date, n=2)
            else:
                return Match.objects.none()

    def get_recommended_teams(self) -> List[RecommendedTeam]:
        score_table = self.__get_competitiontable_cache().score_table
        passed_score_table = []

        for row in score_table:
            if row.get_remaining_matches_count() <= self.cal_at:
                passed_score_table.append(row)

        # point step
        increase_step = 1 / self.cal_at

        first_2 = passed_score_table[0:2]
        almost_relegated = passed_score_table[16:18]

        recommended_teams = []

        # Winner point calculation
        for score_table_row in first_2:
            point = (self.cal_at - score_table_row.get_remaining_matches_count()) * increase_step
            recommended_teams.append(RecommendedTeam(score_table_row.team, point))

        # Relegation point calculation
        for score_table_row in almost_relegated:
            point = (self.cal_at - score_table_row.get_remaining_matches_count()) * increase_step
            recommended_teams.append(RecommendedTeam(score_table_row.team, point))

        return recommended_teams

    def get_recommended_matches(self):
        # for holding results and retrive same results
        recommended_matches: Dict[int, RecommendedResult] = {}

        def get_recommended_result(match_id: int, match: Match) -> RecommendedResult:
            try:
                return recommended_matches[match_id]
            except KeyError:
                result = RecommendedResult(match)
                recommended_matches[match_id] = result
                return result

        derby_matches = self.__get_derby_matches()

        for derby_match in derby_matches:
            result = get_recommended_result(derby_match.id, derby_match)
            result.point += 0.5
            result.add_recommend_method(RecommendedResult.DERBY_MATCHES)

        top_teams_matches = self.__get_top_teams_matches()

        for top_team_match in top_teams_matches:
            result = get_recommended_result(top_team_match.id, top_team_match)
            result.point += 0.5
            result.add_recommend_method(RecommendedResult.TOP_TEAMS)

        low_teams_matches = self.__get_almost_relegated_teams_matches()

        for low_team_match in low_teams_matches:
            result = get_recommended_result(low_team_match.id, low_team_match)
            result.point += 0.5
            result.add_recommend_method(RecommendedResult.ALMOST_RELEGATED_TEAMS)

        winner_decide_matches = self.__get_winner_decide_matches()

        for winner_decide_match in winner_decide_matches:
            result = get_recommended_result(winner_decide_match.id, winner_decide_match)
            result += 1
            result.add_recommend_method(RecommendedResult.WINNER_DECIDE_MATCHES)

        relegation_decide_matches = self.__get_relegattion_decide_matches()

        for relegation_decide_match in relegation_decide_matches:
            result = get_recommended_result(relegation_decide_match.id, relegation_decide_match)
            result += 0.5
            result.add_recommend_method(RecommendedResult.RELEGATION_DECIDE_MATCHES)

        return recommended_matches.values()
