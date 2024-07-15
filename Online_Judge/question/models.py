from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
# Create your models here.


class questions(models.Model):
    question_ID = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 1000)
    Tag = models.CharField(max_length = 100)
    Difficulty = models.CharField(max_length = 10)
    Description = models.TextField()
    def __str__(self):
        return self.Name
    
class testcases(models.Model):
    question = models.ForeignKey(questions, on_delete = models.CASCADE, related_name = 'testcases')
    Test_ID = models.IntegerField(primary_key=True)
    Input = models.TextField()
    Output = models.TextField()
    
    

