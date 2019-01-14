from collections import Counter
from typing import List, Dict, Tuple
from django.contrib.auth.models import User
from django.db.models import Subquery, QuerySet, Q
from django.utils import timezone
from website.models import UserWatchHistory, Match, Team
from ..models import RecommendedMatch


def get_this_user_favorite_teams(user) -> List[Team]:
    watched_matches = (Match
                       .objects
                       .filter(id__in=Subquery(UserWatchHistory.objects.filter(user=user).values('match'))))

    watched_teams_count = Counter()

    for watched_match in watched_matches:
        watched_teams_count.update((watched_match.home_team, watched_match.away_team))

    fovorite_teams = []
    # find number of match that each team play
    for team, count in watched_teams_count.items():
        team_play_count = Match.objects.filter(status=Match.FINISHED).filter(Q(home_team=team) | Q(away_team=team)).count()

        # more than 80% ?
        if count * team_play_count / 100 >= 0.8:
            fovorite_teams.append(team)

    return fovorite_teams


class CollaborativeRecommender:
    def __init__(self, at_date=timezone.now()):
        self.at_date = at_date

    def get_collaborative_recommendation(self) -> Dict[User, List[Tuple[Match, float]]]:
        ''' Return list of RecommendedMatch associate with specific user '''
        users_favorite_teams = self.__find_favorite_teams_of_users()

        # now we got each user with favorite team
        # if there is only 1 user who has favorite team then do not continue collaborative filtering
        if len(users_favorite_teams) <= 1:
            # TODO: what should I return in this case
            return {}

        collaborative_recommended_matches = {}

        for user, favorite_teams in users_favorite_teams.items():
            copy = users_favorite_teams.copy()
            del copy[user]
            similar_users_on_teams = self.__find_similar_users_on_teams((user, favorite_teams), copy)

            # since 'similar_users_on_teams' and given user are similar
            # we can recommend matches for everyone using data from each similar user
            recommended_matches = self.__get_recommended_matches_from_similar_users(user, similar_users_on_teams.keys())

            if recommended_matches:
                collaborative_recommended_matches[user] = recommended_matches

        return collaborative_recommended_matches

    def __find_favorite_teams_of_users(self) -> Dict[User, List[Team]]:
        ''' Iterate over all users in system and find favorite team for each user '''
        all_users = User.objects.all()

        user_with_favorite_teams = {}

        for user in all_users:
            favorite_teams = get_this_user_favorite_teams(user)

            # only those who has favorite teams
            if favorite_teams:
                user_with_favorite_teams[user] = favorite_teams

        return user_with_favorite_teams

    def __find_similar_users_on_teams(self, given_user: Tuple[User, List[Team]], other_users: Dict[User, List[Team]]):
        ''' Return Dictionary where key is a similar user and value is a list of teams that make them similar '''
        similar_users_on_teams = {}

        for other_user, favorite_teams in other_users.items():
            # find common teams i.e. team that both of them like
            both_like = list(set(given_user[1]).intersection(favorite_teams))

            # if no common team then continue next other user
            if not both_like:
                continue

            similar_users_on_teams[other_user] = both_like
        return similar_users_on_teams

    def __get_recommended_matches_from_similar_users(self, given_user, users) -> List[Tuple[Match, float]]:
        other_users_recommended_matches = (RecommendedMatch
                                           .objects
                                           .filter(match__date__gt=self.at_date)
                                           .filter(match__id__in=Subquery(RecommendedMatch.objects.filter(Q(recommendatoin_type=RecommendedMatch.CONTENTBASED) & Q(user__in=users)).values('match')))
                                           .exclude(id__in=Subquery(RecommendedMatch.objects.filter(Q(recommendatoin_type=RecommendedMatch.CONTENTBASED) & Q(user=given_user)).values('match')))
                                           .distinct()
                                           .select_related('match'))

        return [(recommended_match_entry.match, recommended_match_entry.value) for recommended_match_entry in other_users_recommended_matches]
