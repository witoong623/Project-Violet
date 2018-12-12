from datetime import date
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from core.recommendation.common import get_competition_table
from core.recommendation.rulebased import RuleBasedRecommendationEngine
from website.models import Competition


def index(request):
    return HttpResponse('score based recommendation')


def score_table(request):
    premier_league = Competition.objects.select_related('current_season').get(id=2021)
    st = get_competition_table(premier_league, timezone.now())
    context = {
        'teams_count': len(st.score_table),
        'league_table': st.score_table
    }

    return render(request, 'scorebasedrecommend/score-table.html', context=context)


def recommended_teams(request):
    premier_league = Competition.objects.select_related('current_season').get(id=2021)
    rb = RuleBasedRecommendationEngine(premier_league, cal_at=23)
    recommended_teams = rb.get_recommended_teams()

    context = {
        'recommended_teams': recommended_teams,
    }

    return render(request, 'scorebasedrecommend/recommended-teams.html', context=context)


def recommended_matches(request):
    premier_league = Competition.objects.get(id=2021)
    rb = RuleBasedRecommendationEngine(premier_league)
    recommended_matches = rb.get_recommended_matches()

    context = {
        'recommended_matches': recommended_matches
    }

    return render(request, 'scorebasedrecommend/recommended-matches.html', context=context)
