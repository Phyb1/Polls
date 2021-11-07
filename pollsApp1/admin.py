from django.contrib import admin
from django.db import models
from .models import Question, Choice
# Register your models here.

# admin.site.register(Choice) y of doing itinefficient wa
#class ChoiceInline(admin.StackedInline): # adding choice to questions rather than using ...register(Choice)
class ChoiceInline(admin.TabularInline): # this is a more suitable formar as its compact and table like
    model = Choice # stackedInline takes more spaces
    extra = 3 # this is the default number of choices

class QuestionAdmin(admin.ModelAdmin):
    #use field sets to customize arrangemnt of field
    fieldsets = [
        (None, {'fields' : ['question_text']}),
        ('Date Published', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    # fields = ['pub_date', 'question_text'] # customising the admin site
    list_display = ('question_text', 'pub_date', 'was_published_recently') # displaying columns of indvidual fields
    list_filter = ['pub_date'] # adding a filter that display as a side bar enables users to filter by `pub-date`
    search_fields = ['question_text']
admin.site.register(Question, QuestionAdmin)
