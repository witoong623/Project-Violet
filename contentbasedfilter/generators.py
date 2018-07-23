from collections import Counter
from datetime import datetime
from datetime import time
from . import dbutil

WEEKDAY = 1
WEEKEND = 2

class UserProfileGenerator:
    # times used to compare in range
    def get_user_profile(self, user_id, until, use_league=True, use_player=True, use_time=True):
        # matches is list of matches' ID that user watched
        matches = None
        generate_query = ''

        db = dbutil.get_database()
        # TODO delete this in production
        # this code is used to fetch match schedules to generate user watch data
        with db.cursor() as cursor:
            select_user_watch_query = 'select uwg_query from user_watch_generate_queries where uwg_id=%s'
            cursor.execute(select_user_watch_query, (user_id,))
            generate_query = cursor.fetchone()[0]

            cursor.execute(generate_query, (until,))
            matches = [r[0] for r in cursor.fetchall()]

        # select all data that related to matches that user user watched
        uw_count = len(matches)
        ms_sql = 'select ms_league, ms_team1, ms_team2, ms_time, ms_round from match_schedule where ms_id in %s'
        teams_list = None
        time_list = None
        leagues_list = None
        #rounds_list = None
        with db.cursor() as cursor:
            cursor.execute(ms_sql, (matches,))
            results = cursor.fetchall()
            teams_list = [(r[1], r[2]) for r in results]
            leagues_list = [r[0] for r in results]
            time_list = [is_weekday_or_weekend(r[3]) for r in results]
            #rounds_list = [r[3] for r in results]
        db.close()
        
        players_list = []
        if use_player:
            player_sql = 'select p_id from player where (t_id=%s or t_id=%s) and active_flag=1'
            for teams in teams_list:
                players_list.append(self.get_teams_player(player_sql, teams))

        # in each attribute, count duplicate value
        # TODO use use_* to efficently count
        league_counter = Counter()
        team_counter = Counter()
        player_counter = Counter()
        time_counter = Counter()
        #round_counter = Counter()
        for i in range(uw_count):
            league_counter.update((leagues_list[i],))
            team_counter.update(teams_list[i])
            player_counter.update(players_list[i])
            time_counter.update((time_list[i],))
            #round_counter.update((rounds_list[i],))

        # make user profile
        userprofile = UserProfile(user_id)
        # leagues calculation
        if use_league:
            for league, count in league_counter.items():
                pc = count / uw_count * 100
                userprofile.leaguesmatrix[league] = pc
        
        # teams calculation
        for team, count in team_counter.items():
            pc = count / uw_count * 100
            userprofile.teamsmatrix[team] = pc
        
        # players calculation
        if use_player:
            for player, count in player_counter.items():
                pc = count / uw_count * 100
                userprofile.playersmatrix[player] = pc
        
        # time calculation
        if use_time:
            for each_time, count in time_counter.items():
                pc = count / uw_count * 100
                userprofile.timematrix[each_time] = pc

        # rounds calculation
        #for rd, count in round_counter.items():
        #    pc = count / uw_count * 100
        #    userprofile.roundsmatrix[rd] = pc

        return userprofile

    def get_teams_player(self, query, args):
        db = dbutil.get_database()
        try:
            with db.cursor() as cursor:
                cursor.execute(query, args)
                results = cursor.fetchall()
                return [r[0] for r in results]
        finally:
            db.close()

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.leaguesmatrix = dict()
        self.teamsmatrix = dict()
        self.playersmatrix = dict()
        self.timematrix = dict()
        self.roundsmatrix = dict()

    def __str__(self):
        string = 'Leagues\n{}\nTeams\n{}\nPlayers\n{}\nRounds\n{}'.format(self.leaguesmatrix,
            self.teamsmatrix, self.playersmatrix, self.roundsmatrix)
        return string


def get_match_profile(match_id, use_league=True, use_player=True, use_time=True):
    ''' Return match profile of specific match id '''
    #sql = 'select ms_league, ms_team1, ms_team2, ms_round from match_schedule where ms_id=%s'
    sql = 'select ms_league, ms_team1, ms_team2, ms_time from match_schedule where ms_id=%s'
    db = dbutil.get_database()
    ms_result = None
    with db.cursor() as cursor:
        cursor.execute(sql, (match_id,))
        ms_result = cursor.fetchone()
    sql = 'select p_id from player where (t_id=%s or t_id=%s) and active_flag=1'
    players = None
    with db.cursor() as cursor:
        cursor.execute(sql, (ms_result[1], ms_result[2]))
        players = [r[0] for r in cursor.fetchall()]
    db.close()

    mp = MatchProfile(match_id)
    mp.leaguesmatrix = ms_result[0]
    mp.teamsmatrix = (ms_result[1], ms_result[2])
    mp.playersmatrix = players
    mp.timematrix = is_weekday_or_weekend(ms_result[3])
    #mp.roundsmatrix = ms_result[3]
    return mp

class MatchProfile:
    ''' MatchProfile holds matrix of specific match, values in lists represent attribute name
        and every attribute have value 1 '''
    def __init__(self, match_id):
        self.match_id = match_id
        self.leaguesmatrix = 0
        self.teamsmatrix = tuple()
        self.playersmatrix = list()
        self.timematrix = 0
        self.roundsmatrix = 0

def is_weekday_or_weekend(dt):
    if dt.weekday() < 5:
        return WEEKDAY
    else:
        return WEEKEND
