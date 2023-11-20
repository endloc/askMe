from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=32)
    avatar = models.ImageField()
    

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-rating')


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='questions')
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='QuestionLike', related_name='liked_questions')

    questions = QuestionManager()

    # class Meta:
    #     verbose_name = 'question'
    #     verbose_name_plural = 'questions'


# class QuestionTag(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='answers')
    text = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='AnswerLike', related_name='liked_answers')

    answers = models.Manager()

    # class Meta:
    #     verbose_name = 'answer'
    #     verbose_name_plural = 'answers'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')
