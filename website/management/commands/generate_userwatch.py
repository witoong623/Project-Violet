from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from website.models import Team, Match, UserWatchHistory


class Command(BaseCommand):
    help = 'Generate UserWatchHistory of specified team for user specify by email'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='?', type=str)
        parser.add_argument('team_id', nargs='?', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email=options['email'])
        except User.DoesNotExist:
            raise CommandError('The user with email {} doesn\'t exist'.format(options['email']))

        try:
            team = Team.objects.get(id=options['team_id'])
        except Team.DoesNotExist:
            raise CommandError('The team with id {} doesn\'t exist'.format(options['team_id']))

        now = timezone.now()
        matches = Match.objects.filter((Q(home_team=team) | Q(away_team=team)) & Q(date__lt=now))
        self.stdout.write('There are {} matches'.format(len(matches)))

        user_watches = []

        for match in matches:
            user_watch = UserWatchHistory(user=user, match=match)
            user_watches.append(user_watch)

        UserWatchHistory.objects.bulk_create(user_watches)

        self.stdout.write('Successfully generated user watch history')
