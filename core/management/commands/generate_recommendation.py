from django.contrib.auth.models import User
from django.db.models import Count
from django.core.management.base import BaseCommand, CommandError
from website.models import Competition
from ...models import RecommendedMatch
from ...recommendation.contentbased import CosineSimilarity
from ...recommendation.rulebased import RuleBasedRecommendationEngine


class Command(BaseCommand):
    help = 'Generate recommended matches for every user and store in DB'

    def handle(self, *args, **options):
        users = User.objects.annotate(user_watch_count=Count('user_watches')).filter(user_watch_count__gt=0)

        for user in users:
            cosine = CosineSimilarity(user)
            recommended_matches = cosine.get_recommended_matches()

            if recommended_matches is None:
                continue

            insert_recommended_matches = []

            for recommended_match in recommended_matches:
                recommended_match_object = RecommendedMatch(
                    user=user,
                    match=recommended_match[0],
                    recommendatoin_type=RecommendedMatch.CONTENTBASED,
                    value=recommended_match[1]
                )
                insert_recommended_matches.append(recommended_match_object)

            RecommendedMatch.objects.filter(user=user).delete()
            RecommendedMatch.objects.bulk_create(insert_recommended_matches)

        self.stdout.write('Successfully generated recommendation for {} users'.format(len(users)))

        self.stdout.write('Generating recommedation from rule based')
        RecommendedMatch.objects.filter(recommendatoin_type=RecommendedMatch.RULEBASED).delete()

        premier_league = Competition.objects.get(id=2021)
        rb = RuleBasedRecommendationEngine(premier_league)

        rb_recommended_matches = rb.get_recommended_matches()

        insert_rb_recommended_matches = []

        for rb_recommended_match in rb_recommended_matches:
            rb_recommended_match_object = RecommendedMatch(
                match=rb_recommended_match.match,
                recommendatoin_type=RecommendedMatch.RULEBASED,
                value=rb_recommended_match.point
            )
            insert_rb_recommended_matches.append(rb_recommended_match_object)

        RecommendedMatch.objects.bulk_create(insert_rb_recommended_matches)
        self.stdout.write('Successfully generated rule-based recommendation')
