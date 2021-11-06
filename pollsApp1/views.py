from django.http import HttpResponse, HttpResponseRedirect # takes only one argument which is the url the user will be redirected to
from django.template import loader
from django.shortcuts import render, get_object_or_404 # the shortcut for catching errors
from django.urls import reverse

from .models import Question, Choice
# Create your views here.
def index(request):
    '''latest_question_list = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list':latest_question_list}
    return HttpResponse(template.render(context, request))
    '''
    # you can use the below shortcut render to achieve the same in above
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)
  

def index2(request):
     
    return HttpResponse('Hello, world. You are at the polls index' )

def detail(request, question_id):
    # use get() and raise Http404 if the object doesn’t exist. Django provides a shortcut.
    # the detail() view, rewritten
    question = get_object_or_404(Question, pk=question_id)
    '''
    try:
        question = Question.objects.get(pk=question_id)
        #question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: # : The view raises the Http404 exception if a question with the requested ID doesn’t exist.
        raise Http404('Quetsion does not exist')
    '''
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    response = 'You are looking at the results of question %s'
    return HttpResponse(response %question_id )

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_sett.get(pk=request.POST['choice']) # request.POST is a dictionary-like object that lets you access submitted data by keyname
    except (KeyError, Choice.DoesNotExist):
        # display the question voting form
        return render(request, 'polls/detail.html', {'question':question, 'error_message':'You didn\'t select a choice'})
    else:
        selected_choice +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data
        # this prevents the form from being posted twice if the user hits the back Button
        return HttpResponseRedirect(reverse('polls:results'),args=(question.id,))
    # We are using the reverse() function in the HttpResponseRedirect constructor in this example. This function
    # helps avoid having to hardcode a URL in the view function.
