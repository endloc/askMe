from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(max_length=255, blank=True)
    

class QuestionManager(models.Manager):
    def new(self):
        return super().get_query_set().order_by('-date')

    def hot(self):
        return super().get_query_set().order_by('-rating')

    def by_tag(self, tag):
        return super().get_query_set().filter(tags__name=tag)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='questions')
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='QuestionLike', related_name='liked_questions')
    likes_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    # class Meta:
    #     verbose_name = 'question'
    #     verbose_name_plural = 'questions'


# class QuestionTag(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='answers')
    text = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='AnswerLike', related_name='liked_answers')
    likes_count = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.text[:min(70, len(self.text))] + "..."

    # class Meta:
    #     verbose_name = 'answer'
    #     verbose_name_plural = 'answers'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')
