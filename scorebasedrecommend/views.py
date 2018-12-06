from datetime import date
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from .leaguetable import get_score_table
from website.models import Competition


def index(request):
    return HttpResponse('score based recommendation')


def test(request):
    premier_league = Competition.objects.select_related('currentSeason').get(id=2021)
    st = get_score_table(premier_league, timezone.now())
    context = {
        'teams_count': len(st),
        'league_table': st
    }

    return render(request, 'scorebasedrecommend/test.html', context=context)
