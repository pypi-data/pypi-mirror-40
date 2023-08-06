from django.db import models

# Create your models here.
import datetime

from django.db import models
from django.utils import timezone



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True
        was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

'''
Question是个list,它的choice_set也是一个list
#导入
>>> from polls.models import Choice, Question  
#查询Question所有list
>>> Question.objects.all()  
>>> from django.utils import timezone

#创建新的Question
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()

#获取 参数（id是自增长的）
>>> q.id
>>> q.question_text
>>> q.pub_date
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()

#查询id=1的Question
>>> Question.objects.filter(id=1)

#question_text以what开头的Question
>>> Question.objects.filter(question_text__startswith='What')

#查询今年的Question
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

#查询主键为1的Question
>>> Question.objects.get(pk=1)
<Question: What's up?>

>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()

操作Question中choice_set
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()

创建choice_set
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

>>> c.question
<Question: What's up?>

>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
'''