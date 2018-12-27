from django.test import TestCase
from django.contrib.auth.models import User
from ..recommendation.collaborative import CollaborativeRecommender


class CollaborativeTest(TestCase):
    fixtures = ['websitefixture.json']

    def test_no_exception(self):
        recommender = CollaborativeRecommender()
        recommender.get_collaborative_recommendation()
