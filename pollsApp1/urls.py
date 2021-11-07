from django.urls import path
'''urls for pollsApp1'''
from .import views
app_name='polls' # so that django knows from which pattern is the link made from
urlpatterns = [
    # exaample; /polls/
    path('', views.index, name='index'), # the homepage
    # example: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'), # to change the links simple edit the named url pattern
    # example: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # example: polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'), # the name attr is used by ht {% url %} tag to create links for the pattern

]   