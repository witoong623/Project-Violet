import math
from datetime import datetime
from collections import Counter
from django.db.models import Q
from recommendation.models import MatchSchedule


def identify_like_teams(user_watch, until=None):
    ''' user_watch is list of matches' id '''
    if until is None:
        until = datetime.now()

    # get how many matches each team already played
    all_matches = MatchSchedule.objects.filter(Q(ms_league=1) & Q(ms_time__lt=until))
    teams_played_counter = Counter()

    for match in all_matches:
        teams_played_counter.update((match.ms_team1.t_id,))
        teams_played_counter.update((match.ms_team2.t_id,))

    # get how many matches each team played in user watch
    user_watch_team_count = Counter()

    for match_id in user_watch:
        match = MatchSchedule.objects.get(ms_id=match_id)
        user_watch_team_count.update((match.ms_team1.t_id,))
        user_watch_team_count.update((match.ms_team2.t_id,))

    # find teams' id that user like
    like_teams = []

    for team_id, count in teams_played_counter.items():
        if user_watch_team_count[team_id] >= math.floor(count * 0.8):
            like_teams.append(team_id)

    return like_teams


def identify_teams_id_with_matches_id(user_watch, until=None):
    ''' user_watch is list of matches' id\n
        return dictionary where key is team's id and value is a list of matches' id\n
        that team already played '''
    teams_matches = {}

    for match_id in user_watch:
        match = MatchSchedule.objects.get(ms_id=match_id)

        if match.ms_team1.t_id in teams_matches:
            teams_matches[match.ms_team1.t_id].append(match_id)
        else:
            teams_matches[match.ms_team1.t_id] = []
            teams_matches[match.ms_team1.t_id].append(match_id)

        if match.ms_team2.t_id in teams_matches:
            teams_matches[match.ms_team2.t_id].append(match_id)
        else:
            teams_matches[match.ms_team2.t_id] = []
            teams_matches[match.ms_team2.t_id].append(match_id)

    return teams_matches


def calculate_jaccard(base_user_watch, compared_user_watch, like_teams, until=None):
    ''' base_user_watch and compared_user_watch are list of matches' id \n
        like_teams is list of teams' id '''
    if until is None:
        until = datetime.now()

    base_user_teams_played = identify_teams_id_with_matches_id(base_user_watch, until=until)
    compared_user_teams_played = identify_teams_id_with_matches_id(compared_user_watch, until=until)

    teams_jaccard_values = {}

    for like_team_id in like_teams:
        base_set = set(base_user_teams_played[like_team_id])
        compared_set = set(compared_user_teams_played.get(like_team_id, list()))

        jacc_val = len(base_set.intersection(compared_set)) / len(base_set.union(compared_set))
        teams_jaccard_values[like_team_id] = jacc_val

    return teams_jaccard_values
