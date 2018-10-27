from typing import Iterable
from django.contrib.auth.models import User
from website.models import Match, UserWatchHistory


def get_user_watched_matches(user):
    return UserWatchHistory.objects.filter(user=user).values('match')
