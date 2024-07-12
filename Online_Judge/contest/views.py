from django.shortcuts import render
from contest.models import Contests
# Create your views here.

def show_contest(request, contest_id):
    contest = Contests.objects.get(pk = contest_id)
    context = {"Contest" : contest, 'User' : request.user}    
    return render(request, 'contest_page.html', context= context)