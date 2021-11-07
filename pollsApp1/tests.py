from django.contrib.sessions.backends.base import CreateError
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
import datetime


from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question (self):
        '''
        was published recently returns false for questions ehose pub-date 
        is a future date
        '''
        time = timezone.now() + datetime.timedelta(days=100)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was published recently returns false for questions ehose pub-date 
        is older than day one
        '''
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        '''
        was published recently returns false for questions ehose pub-date 
        is within the last day
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    '''
    create a question with a given `question_text` and publishes the given number of `days`
    offset for the number of days to now (negative for questions published in the 
    past and positive for questions that are yet to be published in the future) 
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    '''
    testing views , using the tests to tell a story of admin input and user experience on the site, 
    and checking that at every state and for every new change in the state of the system, 
    the expected results are published
    '''
    def test_no_questions(self):
        '''
        if no questions exist an appropriate message is displayed
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No questions are available')
        self.assertQuerysetEqual(response.content['latest_question_list'], [])


    def test_past_questions(self):
        '''
        questions with a `pub_date` in the past are displayed on the index page
        '''
        question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_futute_questions(self):
        '''
        questions with a `pub_date in the future are not displayed on the 
        index page
        '''
        question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No questions are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_future_questions_and_past_questions(self):
        '''
        even if both future and past questions exist only questions with a past date 
        are displayed 
        '''
        question = create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_two_past_questions(self):
        '''
        the question index page may display multiple questions
        '''
        question1 = create_question(question_text='Past question', days=-30)
        question2 = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question1, question2])
