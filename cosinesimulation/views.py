from datetime import timedelta, datetime
from urllib.parse import parse_qs
from distutils.util import strtobool
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.db.models import Q
from recommendation.models import MatchSchedule
from contentbasedfilter.recommendationengine import CosineSimilarity

COLORS = [
    '#FF1E1E',
    '#FF840A',
    '#FF8E1E',
    '#84FF0A',
    '#0AFF84',
    '#0AFFFF',
    '#0A84FF',
    '#0A0AFF',
    '#840AFF',
    '#FF0AFF',
    '#FF0A84',
    '#D92A2A',
    '#D9822A',
    '#D9D92A',
    '#82D92A',
    '#2AD92A',
    '#2AD982',
    '#2AD9D9',
    '#2A82D9',
    '#2A2AD9',
    '#822AD9',
    '#D92AD9',
    '#D92A82',
    '#840000',
    '#FF4747',
    '#FFA347',
    '#FFFF47',
    '#A3FF47',
    '#47FF47',
    '#47FFA3',
    '#47FFFF',
    '#47A3FF',
    '#4747FF',
    '#A347FF',
    '#FF47FF',
    '#FF47A3',
    '#333333',
    '#FF93F7'
]

UFT = {
    'u1': 19,
    'u11': [19, 1]
}

def index(request):
    u1_matches = MatchSchedule.objects.filter(Q(ms_team1__exact=19) | Q(ms_team2__exact=19))
    u1_match_times = [match.ms_time for match in u1_matches]

    u11_matches = MatchSchedule.objects.filter(Q(ms_team1__exact=19) | Q(ms_team2__exact=19) |
        Q(ms_team1__exact=1) | Q(ms_team2__exact=1))
    u11_match_times = [match.ms_time for match in u11_matches]

    u12_matches = MatchSchedule.objects.filter(Q(ms_team1__exact=19) | Q(ms_team2__exact=19) |
        Q(ms_team1__exact=1) | Q(ms_team2__exact=1) | Q(ms_team1__exact=13) | Q(ms_team2__exact=13))
    u12_match_times = [match.ms_time for match in u12_matches]

    available_simulatoins = {
        'u1': u1_match_times,
        'u11': u11_match_times,
        'u12': u12_match_times
    }
    context = {
        'available_simulations': available_simulatoins
    }

    return render(request, 'cosinesimulation/index.html')

def simulation_data(request):
    u1_matches = MatchSchedule.objects.filter(Q(ms_team1__exact=19) | Q(ms_team2__exact=19)).order_by('ms_time')

    u11_matches = MatchSchedule.objects.filter(Q(ms_team1__exact=19) | Q(ms_team2__exact=19) |
        Q(ms_team1__exact=1) | Q(ms_team2__exact=1)).order_by('ms_time')

    per_user_data = { 'u1': [], 'u11': [] }

    # build u1 data
    for index, match in enumerate(u1_matches, start=1):
        msg = '{} : {} VS {}'.format(datetime.strftime(match.ms_time, '%a %d %b %Y'), match.ms_team1.t_shortname, match.ms_team2.t_shortname)
        per_user_data['u1'].append({'id': match.ms_id,'text': msg})
    
    # build u11 data
    for index, match in enumerate(u11_matches, start=1):
        msg = '{} VS {}'.format(match.ms_team1.t_shortname, match.ms_team2.t_shortname)
        per_user_data['u11'].append({'id': match.ms_id,'text': msg})

    return JsonResponse(per_user_data)

def simulate(request):
    try:
        user_id = request.GET['userId']

        if user_id == 'u1':
            return onefavorite(request)
        elif user_id == 'u11':
            return twofavorite(request)

        raise Http404('user ID {} isn\'t available for simulation'.format(user_id))
    except KeyError:
        raise Http404('sample user_id doesn\'t exist, whole query string is {}'.format(request.GET.urlencode()))

def onefavorite(request):
    try:
        user_id = request.GET['userId']
        until_match_ids = [int(s) for s in request.GET.getlist('untilMatches')]
        useleague = strtobool(request.GET['useLeague'])
        useplayer = strtobool(request.GET['usePlayer'])
        usetime = strtobool(request.GET['useTime'])

    except KeyError as err:
        return HttpResponseBadRequest('parameter {} invalid, whole query string is {}'.format(err, request.GET.urlencode()))

    until_matches = MatchSchedule.objects.filter(ms_id__in=until_match_ids).order_by('ms_time')

    datasets = []
    color_count = 0

    # begin calculate cosine for each remaining matches
    for previous_match in until_matches:
        remaining_matches = MatchSchedule.objects.filter(Q(ms_time__gt=previous_match.ms_time) & (Q(ms_team1=UFT[user_id]) | Q(ms_team2=UFT[user_id])))

        after_time = previous_match.ms_time
        cs_generator = CosineSimilarity(user_id, untildate=after_time, use_league=useleague, use_player=useplayer, use_time=usetime)

        # previous match number, + plus 1 to get next match number
        match_number = 38 - remaining_matches.count() + 1
        after_match = match_number
        data_points = []

        for remain in remaining_matches:
            cs_value = cs_generator.get_user_match_similarity(remain.ms_id)
            data_points.append({'x': match_number, 'y': cs_value})
            match_number += 1

        if data_points:
            dataset = {'label': 'after {}'.format(after_match - 1)}
            dataset['data'] = data_points
            dataset['backgroundColor'] = COLORS[color_count]
            dataset['borderColor'] = COLORS[color_count]
            dataset['fill'] = False

            datasets.append(dataset)
            color_count += 1

    json_object = {
        'labels': [n for n in range(datasets[0]['data'][0]['x'], 39)],
        'datasets': datasets,
        'title': 'case {}'.format(user_id)
    }

    return JsonResponse(json_object)

def twofavorite(request):
    try:
        user_id = request.GET['userId']
        until_match_ids = [int(s) for s in request.GET.getlist('untilMatches')]
        useleague = strtobool(request.GET['useLeague'])
        useplayer = strtobool(request.GET['usePlayer'])
        usetime = strtobool(request.GET['useTime'])

    except KeyError as err:
        return HttpResponseBadRequest('parameter {} invalid, whole query string is {}'.format(err, request.GET.urlencode()))

    until_matches = MatchSchedule.objects.filter(ms_id__in=until_match_ids).order_by('ms_time')

    datasets = []
    color_count = 0

    # begin calculate cosine for each remaining matches
    for previous_match in until_matches:
        remaining_matches = MatchSchedule.objects.filter(((Q(ms_team1=UFT[user_id][0]) | Q(ms_team2=UFT[user_id][0]))
            | (Q(ms_team1=UFT[user_id][1]) | Q(ms_team2=UFT[user_id][1]))) & Q(ms_time__gt=previous_match.ms_time))

        after_time = previous_match.ms_time
        cs_generator = CosineSimilarity(user_id, untildate=after_time, use_league=useleague, use_player=useplayer, use_time=usetime)

        # previous match number, + plus 1 to get next match number
        match_number = 74 - remaining_matches.count() + 1
        after_match = match_number
        data_points = []

        for remain in remaining_matches:
            cs_value = cs_generator.get_user_match_similarity(remain.ms_id)
            data_points.append({'x': match_number, 'y': cs_value})
            match_number += 1

        if data_points:
            dataset = {'label': 'after {}'.format(after_match - 1)}
            dataset['data'] = data_points
            dataset['backgroundColor'] = COLORS[color_count]
            dataset['borderColor'] = COLORS[color_count]
            dataset['fill'] = False

            datasets.append(dataset)
            color_count += 1

    json_object = {
        'labels': [n for n in range(datasets[0]['data'][0]['x'], 75)],
        'datasets': datasets,
        'title': 'case {}'.format(user_id)
    }

    return JsonResponse(json_object)
