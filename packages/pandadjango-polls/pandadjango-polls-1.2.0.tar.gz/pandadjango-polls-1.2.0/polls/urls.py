#!/usr/bin/python
#coding=utf-8
# @TIME  : 2019/01/05 13:31
from django.urls import path
from . import views

app_name = 'polls' #指明操作的app是polls
# urlpatterns = [
#     path('<int:question_id>/index/', views.index, name='index'),
#     path('<int:question_id>/', views.detail, name='detail'), #跳转到detail.html
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
