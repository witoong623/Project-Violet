from typing import Iterable
from django.db.models import Subquery
from django.contrib.auth.models import User
from website.models import Match, UserWatchHistory


def get_user_watched_matches(user):
    return Match.objects.filter(id__in=Subquery(UserWatchHistory.objects.filter(user=user).values('match')))
