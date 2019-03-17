import math
from typing import List, Dict

from django.contrib.auth.models import User
from django.db.models import Count
from django.core.management.base import BaseCommand, CommandError
from website.models import Competition
from ...models import RecommendedMatch
from ...recommendation.contentbased import CosineSimilarity
from ...recommendation.rulebased import RuleBasedRecommendationEngine, RecommendedResult
from ...recommendation.collaborative import CollaborativeRecommender


class RecommendationContainer:
    cb_recommended_matches = None
    cf_recommended_matches = None

    def __init__(self, user):
        self.user = user


class Command(BaseCommand):
    help = 'Generate recommended matches for every user and store in DB'

    def handle(self, *args, **options):
        users = User.objects.annotate(user_watch_count=Count('user_watches')).filter(user_watch_count__gt=0)
        all_recommendations: Dict[str, RecommendationContainer] = {}

        for user in users:
            cosine = CosineSimilarity(user)
            recommended_matches = cosine.get_recommended_matches()

            if recommended_matches is None:
                continue

            cb_recommended_matches = [rb for rb in recommended_matches]

            container = RecommendationContainer(user)
            container.cb_recommended_matches = cb_recommended_matches
            all_recommendations[user.username] = container

        collaborative_recommender = CollaborativeRecommender()
        collaborative_recommended_matches = collaborative_recommender.get_collaborative_recommendation()

        for user, recommended_matches in collaborative_recommended_matches.items():
            cf_recommended_matches = [rb for rb in recommended_matches]
            all_recommendations[user.username].cf_recommended_matches = cf_recommended_matches

        premier_league = Competition.objects.get(id=2021)
        rb = RuleBasedRecommendationEngine(premier_league)
        rb_recommended_matches = rb.get_recommended_matches()

        self.stdout.write('Generate Hybrid between Content-based and Collaborative-filtering recommendation')
        for username, container in all_recommendations.items():
            # delete previous recommended matches
            RecommendedMatch.objects.filter(recommendatoin_type=RecommendedMatch.HYBRID, user=container.user).delete()

            processed_matches_point = []
            if container.cb_recommended_matches is not None:
                for rb in container.cb_recommended_matches:
                    processed_matches_point.append(rb)

            if container.cf_recommended_matches is not None:
                for rb in container.cf_recommended_matches:
                    new_score = rb[1] * 0.9
                    processed_matches_point.append((rb[0], new_score))

            # calculate +1 standard deviation
            mean = sum(rb[1] for rb in processed_matches_point) / len(processed_matches_point)
            std_dev = math.sqrt(sum((mean - rb[1])**2 for rb in processed_matches_point) / len(processed_matches_point))
            first_std_dev = mean + std_dev
            processed_matches_point = list(filter(lambda x: x[1] >= first_std_dev, processed_matches_point))

            insert_user_hybrid_recommended_matches = []
            for processed_match_point in processed_matches_point:
                hybrid_recommended_matches = RecommendedMatch(
                    user=container.user,
                    match=processed_match_point[0],
                    recommendatoin_type=RecommendedMatch.HYBRID,
                    value=processed_match_point[1]
                )
                insert_user_hybrid_recommended_matches.append(hybrid_recommended_matches)
            RecommendedMatch.objects.bulk_create(insert_user_hybrid_recommended_matches)

            self.stdout.write(f'add {len(insert_user_hybrid_recommended_matches)} hybrid recommendation for user {username}')

        # final case, rb before mix
        self.stdout.write('Generate recommendation for rule-based')
        # delete previous recommended matches
        RecommendedMatch.objects.filter(recommendatoin_type=RecommendedMatch.HYBRID, user=None).delete()

        rb_mean = sum(x.point for x in rb_recommended_matches) / len(rb_recommended_matches)
        rb_std_dev = math.sqrt(sum((rb_mean - x.point)**2 for x in rb_recommended_matches) / len(rb_recommended_matches))
        rb_first_std_dev = rb_mean + rb_std_dev
        rb_recommended_matches: List[RecommendedResult] = list(filter(lambda x: x.point >= rb_first_std_dev, rb_recommended_matches))

        insert_rb_recommended_matches = []
        for rb in rb_recommended_matches:
            rb_recommended_match = RecommendedMatch(
                match=rb.match,
                recommendatoin_type=RecommendedMatch.HYBRID,
                value=rb.point
            )
            insert_rb_recommended_matches.append(rb_recommended_match)
        RecommendedMatch.objects.bulk_create(insert_rb_recommended_matches)

        self.stdout.write(f'add {len(insert_rb_recommended_matches)} Rule-based recommendation for display in mixed')
