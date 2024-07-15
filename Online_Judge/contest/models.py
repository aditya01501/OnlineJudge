from django.db import models
from question.models import questions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# Create your models here.

class Contests(models.Model):
    Contest_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length = 1000)
    Questions = models.ManyToManyField(questions, related_name= 'contests')
    Participants = models.ManyToManyField(get_user_model(), related_name= 'contests', null=True)
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)    
    def __str__(self):
        return self.Name
    


class Leaderboard(models.Model):
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.contest.Name} - Total Score: {self.total_score}"
    
class Submission(models.Model):
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.TextField(null= True)
    submission_date = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contests, null=True, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)  # You can adjust the max_length as needed
    language = models.CharField(max_length=20)
    def __str__(self):
        return f"Submission by {self.user.username} for {self.question.Name} - Verdict: {self.verdict}"
    
    
class Score(models.Model):
    ScoreID = models.IntegerField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.question.Name} - {self.contest.Name} - Score: {self.score}"
    

    
