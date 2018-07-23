import math
from .generators import UserProfileGenerator
from .generators import get_match_profile
from recommendation.models import League

class CosineSimilarity:
    def __init__(self, user_id, untildate=None, use_league=True, use_player=True, use_time=True):
        self.user_id = user_id
        self.untildate = untildate
        self.userprofile = None
        self.use_league = use_league
        self.use_player = use_player
        self.use_time = use_time

    def get_user_match_similarity(self, match_id):
        if self.userprofile == None:
            upg = UserProfileGenerator()
            self.userprofile = upg.get_user_profile(self.user_id, self.untildate, use_league=self.use_league, use_player=self.use_player, use_time=self.use_time)
        
        mp = get_match_profile(match_id, use_league=self.use_league,
            use_player=self.use_player, use_time=self.use_time)

        dividend_up_mp = 0
        divisor_up = 0
        divisor_mp = 0
        # find similar league
        if self.use_league:
            if mp.leaguesmatrix in self.userprofile.leaguesmatrix:
                dividend_up_mp += 1 * self.userprofile.leaguesmatrix[mp.leaguesmatrix]
            divisor_mp += 1

        # find similar teams
        for team in mp.teamsmatrix:
            if team in self.userprofile.teamsmatrix:
                dividend_up_mp += 1 * self.userprofile.teamsmatrix[team]
            divisor_mp += 1

        # find similar players
        if self.use_player:
            for player in mp.playersmatrix:
                if player in self.userprofile.playersmatrix:
                    dividend_up_mp += 1 * self.userprofile.playersmatrix[player]
                divisor_mp += 1

        # find similar time
        if self.use_time:
            if mp.timematrix in self.userprofile.timematrix:
                dividend_up_mp += 1 * self.userprofile.timematrix[mp.timematrix]
            divisor_mp += 1

        # find similar round
        #if mp.roundsmatrix in self.userprofile.roundsmatrix:
        #    dividend_up_mp += 1 * self.userprofile.roundsmatrix[mp.roundsmatrix]
        #divisor_mp += 1

        # compute divisor for user profile
        # leagues
        if self.use_league:
            divisor_up += sum(self.userprofile.leaguesmatrix.values())

        # teams
        divisor_up += sum(self.userprofile.teamsmatrix.values())

        # players
        if self.use_player:
            divisor_up += sum(self.userprofile.playersmatrix.values())

        # time
        if self.use_time:
            divisor_up += sum(self.userprofile.timematrix.values())

        # rounds
        #divisor_up += sum(self.userprofile.roundsmatrix.values())

        # find square of divisors
        divisor_up = math.sqrt(divisor_up)
        divisor_mp = math.sqrt(divisor_mp)

        # find cosine similarity
        cs = dividend_up_mp / (divisor_up * divisor_mp)

        return cs

def get_league_name(league_id):
    league = League.objects.get(pk=league_id)
    return league.le_name

def get_team_name(team_id):
    pass

def get_player_name(player_id):
    pass