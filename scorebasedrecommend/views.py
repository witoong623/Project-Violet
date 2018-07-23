from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .leaguetable import get_score_table
from datetime import date

def index(request):
    return HttpResponse('score based recommendation')

def test(request):
    st = get_score_table('premier league', date(2018, 6, 1))
    context = {
        'teams_count': len(st),
        'league_table': st
    }

    return render(request, 'scorebasedrecommend/test.html', context=context)
