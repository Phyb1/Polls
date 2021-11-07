from django.db import models
import datetime
from django.db.models import fields
from django.utils import timezone
from django.contrib import admin
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') # the time setting is UTC it needs to be chnaged to show gmt +2 in the settings.py fileee

    @admin.display( # decorator for the list_display
        boolean=True,
        ordering='pub_date',
        description= 'Published recently',
    )
    def __str__(self): # a string represantions is used everywhere for the model
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now -datetime.timedelta(days=1) <= self.pub_date <= now 


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text