from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(max_length=255, blank=True)


class QuestionManager(models.Manager):
    def new_questions(self):
        return super().get_query_set().order_by('-date')

    def hot_questions(self):
        return super().get_query_set().order_by('-likes_count')

    def questions_by_tag(self, tag):
        return super().get_query_set().filter(tags__name=tag).order_by('-date')


class AnswerManager(models.Manager):
    def answers_by_question(self, required_question):
        # try:
        return self.all().filter(question=required_question).order_by('-date')
        # except self.model.DoesNotExist as e:
        #     return Answer.objects.none()


class TagManager(models.Manager):
    def tag_by_title(self, title):
        return self.filter(tag_title__exact=title)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, related_name="questions")
    date = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField(User, through='QuestionLike', related_name='liked_questions')
    likes_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.id} {str(self.title)}"

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

    def __str__(self):
        return f"to question: {self.question}; from user: {self.user}"


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField(User, through='AnswerLike', related_name='liked_answers')
    likes_count = models.IntegerField(default=0)

    objects = models.AnswerManager()

    def __str__(self):
        return f"to question: {self.question}; answer text: {self.text[:min(40, len(str(self.text)))]} ..."

    # class Meta:
    #     verbose_name = 'answer'
    #     verbose_name_plural = 'answers'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"to answer: {self.answer}; from user: {self.user}"
