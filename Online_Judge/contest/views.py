from django.shortcuts import render
from contest.models import Contests, Score, Leaderboard
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
import time
import json
from django.contrib.auth import get_user_model
from question.models import questions
from datetime import datetime
from django.utils import timezone
# Create your views here.

User = get_user_model()

def show_contest(request, contest_id):
    contest = Contests.objects.get(pk = contest_id)
    now = datetime.now()
    if timezone.is_naive(contest.start_time):
        print("lol")
        event_date_aware = timezone.make_aware(contest.start_time, timezone.get_default_timezone())
    else:
        event_date_aware = contest.start_time

    if timezone.is_naive(now):
        print("lol")
        now = timezone.make_aware(now, timezone.get_default_timezone())
    else:
        now = now
 
    context = {"Contest" : contest, 'User' : request.user}    
    if(now < event_date_aware):
        return render(request, 'contest_notstarted.html', context= context)
    else :
        return render(request, 'contest.html', context= context)

def show_leaderboard(request, contest_id):
    contest = Contests.objects.get(pk = contest_id)
    context = {"Contest" : contest, 'User' : request.user}    
    return render(request, 'contest_leaderboard.html', context= context)

def register_contest(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        print("registered")
        Contests.objects.all()
        contest_id = data.get('contestId')
        user = data.get('user')
        contest = Contests.objects.get(pk=contest_id)
        user = User.objects.get(pk=user)
        contest.Participants.add(user)
        contest.save()
        for que in contest.Questions.all():
            sco = Score(question=que, contest=contest, user= user, score = 0)
            sco.save()
        ldbrd = Leaderboard(contest=contest, user = user, total_score=0)
        ldbrd.save()
        return JsonResponse({"status" : "success"})   
    else :
        pass

def contest_qna(request, contest_id, question_id):
    contest = Contests.objects.get(pk = contest_id)
    question = questions.objects.get(pk = question_id)
    context = {"Contest" : contest, "question" : question}
    return render(request, 'contest_question.html', context= context)
    pass

def get_leaderboard(request, contest_id):
    contest = get_object_or_404(Contests, pk=contest_id)
    leaderboard_data = Leaderboard.objects.filter(contest=contest).values('user__username', 'total_score')

    # Convert queryset to list
    leaderboard_list = list(leaderboard_data)

    return JsonResponse(leaderboard_list, safe=False)