from datetime import datetime
from typing import Iterable, List
from django.db.models import Subquery
from django.contrib.auth.models import User
from website.models import Competition, Match, UserWatchHistory


def get_user_watched_matches(user):
    return Match.objects.filter(id__in=Subquery(UserWatchHistory.objects.filter(user=user).values('match')))


class CompetitionTableRow:
    played = 0
    point = 0

    won = 0
    drawn = 0
    lost = 0

    goal_for = 0
    goal_against = 0
    goal_difference = 0

    def get_remaining_matches_count(self):
        # TODO: change constant value 38 to competition specific match
        return 38 - self.played

    def get_best_point(self):
        # TODO: change constant value 3 to competition specific point
        return self.get_remaining_matches_count() * 3 + self.point

    def __init__(self, team, total_matches=38):
        self.team = team
        self.total_matches = total_matches


class CompetitionTable:
    score_table: List[CompetitionTableRow] = []
    played_count = 0
    teams_count = 0

    def __init__(self, competition_name: str, season: str, at_date: datetime):
        self.at_date = at_date
        self.competition_name = competition_name
        self.season = season


def get_competition_table(competition: Competition, at_date: datetime) -> CompetitionTable:
    st = CompetitionTable(competition.name, competition.current_season.display_name, at_date)

    matches_until = Match.objects.select_related('home_team', 'away_team').filter(date__lt=at_date)
    st.played_count = matches_until.count()

    teams = competition.current_season.teams.all()
    st.teams_count = teams.count()

    # init dict of score table and teams
    temp_score_table = {}
    for team in teams:
        temp_score_table[team.id] = CompetitionTableRow(team)

    for match in matches_until:
        if match.status != Match.FINISHED:
            continue

        home_id = match.home_team.id
        away_id = match.away_team.id

        # calculate point, won, drawn and lost
        if match.home_score > match.away_score:
            # case home team win
            temp_score_table[home_id].point += 3

            temp_score_table[home_id].won += 1
            temp_score_table[away_id].lost += 1
        elif match.away_score > match.home_score:
            # case away team win
            temp_score_table[away_id].point += 3

            temp_score_table[away_id].won += 1
            temp_score_table[home_id].lost += 1
        else:
            # case draw
            temp_score_table[home_id].point += 1
            temp_score_table[away_id].point += 1

            temp_score_table[home_id].drawn += 1
            temp_score_table[away_id].drawn += 1

        # increase played field
        temp_score_table[home_id].played += 1
        temp_score_table[away_id].played += 1

        # goal for and goal against
        temp_score_table[home_id].goal_for += match.home_score
        temp_score_table[home_id].goal_against += match.away_score

        temp_score_table[away_id].goal_for += match.away_score
        temp_score_table[away_id].goal_against += match.home_score

        # calculate goal difference
        temp_score_table[home_id].goal_difference += match.home_score - match.away_score
        temp_score_table[away_id].goal_difference += match.away_score - match.home_score

    st.score_table = sorted(temp_score_table.values(), key=lambda d: (d.point, d.goal_difference), reverse=True)

    return st
