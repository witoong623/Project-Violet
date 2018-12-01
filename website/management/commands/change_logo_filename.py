import os
from django.db.models import Q
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from website.models import Team


class Command(BaseCommand):
    base_path = os.path.join(settings.BASE_DIR, 'website\static\website\images')

    def handle(self, *args, **options):
        teams = Team.objects.all()

        for team in teams:
            current_filename = os.path.join(self.base_path, '{}.png'.format(team.short_name))
            new_filename = os.path.join(self.base_path, '{}.png'.format(team.name))
            os.rename(current_filename, new_filename)

        self.stdout.write('Change all file names successfully')
