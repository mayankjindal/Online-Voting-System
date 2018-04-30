from django.shortcuts import render, get_object_or_404
from .models import User, UserProfile, Position, Candidate
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
import base64


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/Vote/home/')
            else:
                return HttpResponseRedirect("Account disabled")
        else:
            print("Invalid credentials: {0}, {1}".format(username, password))
            return HttpResponseRedirect("Invalid login credentials")
    else:
        return render(request, 'Vote/login.html', {})


@login_required(redirect_field_name='/Vote/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/Vote/home/')


def home(request):
    context = {}
    return render(request, 'Vote/home.html', context)


def home_hindi(request):
    context = {}
    return render(request, 'Vote/home_hindi.html', context)


def home_german(request):
    context = {}
    return render(request, 'Vote/home_german.html', context)


def home_spanish(request):
    context = {}
    return render(request, 'Vote/home_spanish.html', context)


def vote(request):
    context = {}
    try:
        pos = Position.objects.all()
        user = User.objects.get(username=request.user.username)
        profile = UserProfile.objects.get(user=user)
        context['candidates'] = []
        if profile.voted:
            return HttpResponseRedirect('/Vote/voted/')
        else:
            for c in pos:
                can = []
                candidate = Candidate.objects.filter(candidate=c)
                for i in range(0, c.no_of_candidates):
                    can.append([candidate[i], c.position])
                context['candidates'].append(can)
    except:
        return HttpResponseRedirect("/Vote/login/")
    if request.method == 'POST':
        pos = Position.objects.all()
        for c in pos:
            s = 'candidate' + c.position
            selected_candidate = Candidate.objects.get(pk=request.POST[s])
            selected_candidate.votes += 1
            selected_candidate.save()
            profile.voted = True
            profile.save()
        else:
            print("No Post")

    return render(request, 'Vote/vote.html', context)


def results(request):
    context = {}
    pos = Position.objects.all()
    context['candidates'] = []
    for c in pos:
        fig = plt.figure()
        vot = []   # No of votes for graph
        can = []
        cand = []  # Name of the candidates for graph labelling
        candidate = Candidate.objects.filter(candidate=c)
        for i in range(0, c.no_of_candidates):
            can.append([candidate[i]])
            cand.append(candidate[i].name)
            vot.append(candidate[i].votes)
            
        plt.pie(vot, labels=cand, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        name = "/home/mayank/HCI/Vote/static/Vote/" + c.position + '.png'
        fig.savefig(name)
        can[0].append(c)
        can[0].append(name)
        plt.close(fig)
        context['candidates'].append(can)

    return render(request, 'Vote/results.html', context)


def about(request):
    context = {}
    return render(request, 'Vote/about.html', context)


def voted(request):
    context = {}
    return render(request, 'Vote/voted.html', context)