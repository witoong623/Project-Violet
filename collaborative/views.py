import random
import numpy as np
import datetime
import math
import jaccardcollaborative.jaccard as jacc
from sklearn.neighbors import NearestNeighbors
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from recommendation.models import MatchSchedule


MAN_U_ID = 19
MAN_CITY_ID = 16


def index(request):
    return HttpResponse('this is collaborative app')


def simulate_fiding_similar_users(request):
    # use u1 who like to watch Man U as a given user that we want to find similar user to him
    all_matches = MatchSchedule.objects.filter(ms_league_id=1)
    u1_watch = []

    for match in all_matches:
        if match.ms_team1.t_id == 19 or match.ms_team2.t_id == 19:
            u1_watch.append(1)
        else:
            u1_watch.append(0)

    # construct users that similar to u1
    sim_users = [u1_watch[:], u1_watch[:]]

    # randomly add another 20% watching to each one which is equal to 76 matches (from 380)
    for user_watch in sim_users:
        for r in range(76):
            while True:
                ran = random.randint(0, 379)
                if user_watch[ran] == 0:
                    user_watch[ran] = 1
                    break
    
    # generate not similar users, watch the same number of matches i.e. 76+38=114
    def zeromaker(n):
        listofzeros = [0] * n
        return listofzeros
    
    not_sim_users = [zeromaker(380) for r in range(10)]

    for user_watch in not_sim_users:
        for r in range(114):
            while True:
                ran = random.randint(0, 379)
                if user_watch[ran] == 0:
                    user_watch[ran] = 1
                    break

    training_users = sim_users + not_sim_users

    readable_training_users = ['T{}'.format(i + 1) for i in range(len(training_users))]

    nbrs = NearestNeighbors(n_neighbors=12, algorithm='auto').fit(np.array(training_users))
    distances, indices = nbrs.kneighbors(np.array([u1_watch]))

    nearest_users = []

    for i in range(len(indices[0])):
        nearest_users.append({'username': readable_training_users[indices[0][i]],
                              'distance': distances[0][i]})

    return render(request, 'collaborative/simulatesimilaruser.html', context={'simulate_results': nearest_users})


def simulate_jaccard(request):
    all_man_u = MatchSchedule.objects.filter(ms_league_id=1).filter(Q(ms_team1=19) | Q(ms_team2=19))
    all_man_u_ids = [m.ms_id for m in all_man_u]

    u1_watch = {m.ms_id for m in all_man_u}

    s1 = u1_watch.copy()
    s2 = u1_watch.copy()

    for r in range(76):
        while True:
            ran = random.randint(0, 379)
            if ran not in s1:
                s1.add(ran)
                break

    for r in range(76):
        while True:
            ran = random.randint(0, 379)
            if ran not in s2:
                s2.add(ran)
                break

    ns_users = []

    for u in range(10):
        ns_user = set()
        for r in range(114):
            while True:
                ran = random.randint(0, 379)
                if ran not in ns_user:
                    ns_user.add(ran)
                    break
        
        ns_users.append(ns_user)

    # start calculating u1 against other users
    results = {}

    results['s1'] = len(u1_watch.intersection(s1)) / len(u1_watch.union(s1))
    results['s2'] = len(u1_watch.intersection(s2)) / len(u1_watch.union(s2))

    for i, ns_user in enumerate(ns_users):
        key = 'ns{}'.format(i + 1)
        results[key] = len(u1_watch.intersection(ns_user)) / len(u1_watch.union(ns_user))

    return render(request, 'collaborative/jaccardsimulatesimilaruser.html', context={'simulate_results': results})


def simulate_jaccard2(request):
    pot = datetime.datetime(2018, 1, 1, 0, 0, 0)
    matches_until = MatchSchedule.objects.filter(Q(ms_league=1) & Q(ms_time__lt=pot))

    user_a = set()

    for match in matches_until:
        if match.ms_team1.t_id == MAN_U_ID or match.ms_team2.t_id == MAN_U_ID:
            user_a.add(match.ms_id)

    # User B generation
    user_b = set()
    a_copy = user_a.copy()
    man_u_90_count = math.floor(len(user_a) * 0.9)

    for i in range(man_u_90_count):
        user_b.add(a_copy.pop())

    man_city_matches = MatchSchedule.objects.filter(Q(ms_league=1) & Q(ms_time__lt=pot)).filter(Q(ms_team1=MAN_CITY_ID) | Q(ms_team2=MAN_CITY_ID))
    man_city_20_count = math.floor(man_city_matches.count() * 0.2)

    for i in range(man_city_20_count):
        user_b.add(man_city_matches[i].ms_id)

    # User C generation
    user_c = set()
    a_copy2 = user_a.copy()
    man_u_50_count = math.floor(len(user_a) * 0.5)
    
    for i in range(man_u_50_count):
        user_c.add(a_copy2.pop())

    man_city_50_count = math.floor(man_city_matches.count() * 0.5)
    
    for i in range(man_city_50_count):
        user_c.add(man_city_matches[i].ms_id)

    # identify what team user A like
    a_like_teams = jacc.identify_like_teams(list(user_a), pot)
    jaccard_with_b = jacc.calculate_jaccard(list(user_a), list(user_b), a_like_teams, pot)
    jaccard_with_c = jacc.calculate_jaccard(list(user_a), list(user_c), a_like_teams, pot)

    context = {
        'base_username': 'A',
        'simulate_results': {
            'B': jaccard_with_b,
            'C': jaccard_with_c
        }
    }

    return render(request, 'collaborative/jaccardsimulatesimilaruser2.html', context)
