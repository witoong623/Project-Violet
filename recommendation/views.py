from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import UserWatch, MatchSchedule, UserWatchGenerateQueries
from contentbasedfilter.recommendationengine import CosineSimilarity
from datetime import datetime

def index(request):
    return render(request, 'recommendation/index.html')

def results(request, user_id, until='2018:01:01'):
    generate_query = UserWatchGenerateQueries.objects.filter(pk=user_id)
    if not generate_query.exists():
        raise Http404("sample user_id doesn't exist")

    untildate = datetime.strptime(until, '%Y:%m:%d')
    sm_generator = CosineSimilarity(user_id, untildate)
    # TODO remove league filter that was added for experiment
    match_schedules = MatchSchedule.objects.filter(ms_time__gt=untildate).filter(ms_league=1)
    similarities = []

    for ms in match_schedules:
        cs = sm_generator.get_user_match_similarity(ms.ms_id)
        similarities.append((ms, cs))

    similarities_des = sorted(similarities, key=lambda result : result[1], reverse=True)
    context = {
        'user_id':user_id,
        'recommend_result': similarities_des,
        'until': untildate,
    }

    return render(request, 'recommendation/results.html', context=context)

def getrecommend(request):
    try:
        user_id = request.POST['user_id']
        until = request.POST['until']

        if until == '':
            return HttpResponseRedirect(reverse('recommendation:results', args=(user_id,)))
        else:
            return HttpResponseRedirect(reverse('recommendation:results', args=(user_id, until)))
    except KeyError:
        raise Http404("sample user_id doesn't exist")

def preference_table(request):
    return render(request, 'recommendation/user_preference.html')
