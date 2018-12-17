from django.db import models
from django.contrib.auth import get_user_model
from website.models import Match


class RecommendedMatch(models.Model):
    CONTENTBASED = 'CONTENTBASED'
    COLLABORATIVE = 'COLLABORATIVE'
    HYBRID = 'HYBRID'
    RULEBASED = 'RULEBASED'
    RECOMMENDATION_TYPE = (
        (CONTENTBASED, 'Content-based'),
        (COLLABORATIVE, 'Collaborative'),
        (RULEBASED, 'Rule-based'),
        (HYBRID, 'Hybrid')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recommended_matches', null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='+')
    recommendatoin_type = models.CharField(max_length=13, choices=RECOMMENDATION_TYPE, default=CONTENTBASED)
    value = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
