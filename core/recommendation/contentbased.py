import math
from collections import Counter
from django.utils import timezone
from .common import get_user_watched_matches
from website.models import Match


WEEKDAY = 1
WEEKEND = 2


def get_user_profile(user):
    '''
    Get profile that describe user football preference
    '''
    watched_matches = get_user_watched_matches(user)
    matches_num = len(watched_matches)

    # convert field to lists
    teams_list = [(match.home_team.id, match.away_team.id) for match in watched_matches]
    competitions_list = [match.competition.id for match in watched_matches]
    times_list = [is_weekday_or_weekend(match.date) for match in watched_matches]

    # counting
    teams_counter = Counter()
    competitions_counter = Counter()
    times_counter = Counter()

    for i in range(matches_num):
        teams_counter.update(teams_list[i])
        competitions_counter.update((competitions_list[i],))
        times_counter.update((times_list[i],))

    # create user profile from counter
    user_profile = UserProfile(user)

    for team, count in teams_counter.items():
        pc = count / matches_num
        user_profile.teamsmatrix[team] = pc

    for competition, count in competitions_counter.items():
        pc = count / matches_num
        user_profile.competitionsmatrix[competition] = pc

    for time, count in times_counter.items():
        pc = count / matches_num
        user_profile.timematrix[time] = pc

    return user_profile


class UserProfile:
    def __init__(self, user):
        self.user = user
        self.competitionsmatrix = dict()
        self.teamsmatrix = dict()
        self.timematrix = dict()


def get_match_profile(id):
    try:
        match = Match.objects.get(id=id)
    except Match.DoesNotExist:
        return None

    match_profile = MatchProfile(id)
    match_profile.competitionmatrix = match.competition.id
    match_profile.teamsmatrix = (match.home_team.id, match.away_team.id)
    match_profile.timematrix = is_weekday_or_weekend(match.date)

    return match_profile


class MatchProfile:
    def __init__(self, id):
        self.id = id
        self.competitionmatrix = 0
        self.teamsmatrix = tuple()
        self.timematrix = 0


class CosineSimilarity:
    def __init__(self, user):
        self.user = user
        self.user_profile = None
        self.cs_baseline = 5

    def get_recommended_matches(self):
        if self.user_profile is None:
            self.user_profile = get_user_profile(self.user)

        upcomming_matches = Match.objects.filter(date__gt=timezone.now())

        recommended_matches = []

        for match in upcomming_matches:
            match_profile = get_match_profile(match.id)

            dividend_up_mp = 0
            divisor_up = 0
            divisor_mp = 0

            if match_profile.competitionmatrix in self.user_profile.competitionsmatrix:
                dividend_up_mp += 1 * self.user_profile.competitionsmatrix[match_profile.competitionmatrix]
            divisor_mp += 1

            for team in match_profile.teamsmatrix:
                if team in self.user_profile.teamsmatrix:
                    dividend_up_mp += 1 * self.user_profile.teamsmatrix[team]
                divisor_mp += 1

            if match_profile.timematrix in self.user_profile.timematrix:
                dividend_up_mp += 1 * self.user_profile.timematrix[match_profile.timematrix]
            divisor_mp += 1

            divisor_up += sum(self.user_profile.competitionsmatrix.values())
            divisor_up += sum(self.user_profile.teamsmatrix.values())
            divisor_up += sum(self.user_profile.timematrix.values())

            divisor_up = math.sqrt(divisor_up)
            divisor_mp = math.sqrt(divisor_mp)

            cs = dividend_up_mp / (divisor_mp * divisor_up)
            recommended_matches.append((match, cs))

        if len(recommended_matches) == 0:
            return None

        return recommended_matches


def is_weekday_or_weekend(dt):
    if dt.weekday() < 5:
        return WEEKDAY
    else:
        return WEEKEND
