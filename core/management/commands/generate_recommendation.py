from django.contrib.auth.models import User
from django.db.models import Count
from django.core.management.base import BaseCommand, CommandError
from ...models import RecommendedMatch
from ...recommendation.contentbased import CosineSimilarity


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
