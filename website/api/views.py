from datetime import timedelta
from django.utils import timezone
from django.db.models import Subquery, QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from ..models import Match, UserWatchHistory
from .serializers import MatchSerialzer, UserWatchHistorySerializer


class UpcommingMatchesList(ListAPIView):
    '''Return all matches from next match day '''
    today = timezone.now()
    queryset = (Match
                .objects
                .filter(match_day=Subquery(Match.objects.filter(date__gt=today).order_by('date').values('match_day')[:1]))
                .filter(status=Match.SCHEDULED)
                .order_by('date'))
    serializer_class = MatchSerialzer


class RecentMatchesList(ListAPIView):
    '''Return latest 4 matches that already played '''
    today = timezone.now()
    queryset = Match.objects.filter(date__lt=today).order_by('-date')[:4]
    serializer_class = MatchSerialzer


class TodayMatchesList(ListAPIView):
    '''Return matches that will be playing today '''
    today_min = timezone.now()
    today_max = today_min + timedelta(days=1)
    queryset = Match.objects.filter(date__range=(today_min, today_max)).order_by('-date')
    serializer_class = MatchSerialzer


class UserWatchHistoryListCreateDestroyAPIView(DestroyModelMixin, ListCreateAPIView):
    '''Return all matches' id of matches that requested user watched/will watch '''
    serializer_class = UserWatchHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = UserWatchHistory.objects.filter(user=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)