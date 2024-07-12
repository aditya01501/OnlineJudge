from django.db import models
from question.models import questions
from django.contrib.auth import get_user_model
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