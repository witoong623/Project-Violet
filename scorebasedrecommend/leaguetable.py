from recommendation.models import MatchSchedule, Team
from django.db.models import Q
from datetime import date

class LeagueTable:
    score_table = []
    played_count = 0
    teams_count = 0

    def __init__(self, league_name, at_date):
        self.at_date = at_date
        self.league_name = league_name

class LeagueTableRow:
    point = 0
    goals = 0
    team_name = ''

    def __init__(self, t_id):
        self.t_id = t_id

# TODO this method is specifically implement for PL
def get_score_table(league_name, at_date):
    st = LeagueTable(league_name, at_date)

    matches_until = MatchSchedule.objects.filter(Q(ms_time__lte=at_date) & Q(ms_league__exact=1))
    st.played_count = matches_until.count()

    pl_teams = Team.objects.filter(Q(t_id__lte=20) & Q(t_id__gte=1))
    st.teams_count = pl_teams.count()

    # init dict of score table and teams
    temp_score_table = {}
    for id in range(1, 21):
        temp_score_table[id] = LeagueTableRow(id)

    for match in matches_until:
        home_id = match.ms_team1.t_id
        away_id = match.ms_team2.t_id

        if match.ms_team1_score > match.ms_team2_score:
            # case home team win
            temp_score_table[home_id].point += 3
        elif match.ms_team2_score > match.ms_team1_score:
            # case away team win
            temp_score_table[away_id].point += 3
        else:
            # case equal
            temp_score_table[home_id].point += 1
            temp_score_table[away_id].point += 1
        
        # calculate goals
        temp_score_table[home_id].goals += match.ms_team1_score - match.ms_team2_score
        temp_score_table[away_id].goals += match.ms_team2_score - match.ms_team1_score

    # add team name to table
    for team_id in temp_score_table.keys():
        team = Team.objects.get(pk=team_id)
        temp_score_table[team_id].team_name = team.t_shortname

    return sorted(temp_score_table.values(), key=lambda d: (d.point, d.goals), reverse=True)
