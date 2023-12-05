import random
import string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from faker import Faker
from app.models import Tag, Question, QuestionLike, Answer, AnswerLike
from itertools import islice

fake = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        # self.create_users(ratio)
        # self.create_tags(ratio)
        self.create_questions(ratio)
        # self.create_answers(ratio)
        # self.create_likes(ratio)
        print(f'END.')

    def create_users(self, ratio):
        for _ in range(ratio):
            try:
                User.objects.create_user(
                    username=fake.first_name()+str(random.randint(1, 1000)),
                    password=get_random_string(length=random.randint(8, 15)))
            except IntegrityError:
                print("user error")
        print(f"{ratio} users finished.")

    def create_tags(self, ratio):
        # tags = [Tag(name=(fake.word() + fake.word())[:20]) for _ in range(ratio)]
        tags = [Tag.objects.create(name=(fake.word()[:random.randint(1, 3)] + fake.word()[:random.randint(2, 5)]) +
                                        fake.word()[:random.randint(1, 4)]) for _ in range(ratio)]
        batch_size = 100
        # while True:
        #     try:
        #         batch = list(islice(tags, batch_size))
        #         if not batch:        batch_size = 100
        #         # while True:
        #         #     try:
        #         #         batch = list(islice(tags, batch_size))
        #         #         if not batch:
        #         #             break
        #         #         Tag.objects.bulk_create(batch)
        #         #     except IntegrityError:
        #         #         continue
        #             break
        #         Tag.objects.bulk_create(batch)
        #     except IntegrityError:
        #         continue
        while True:
            batch = list(islice(tags, batch_size))
            if not batch:
                break
            Tag.objects.bulk_create(batch)
        print(f"{ratio} tags finished.")

    def create_questions(self, ratio):
        users = User.objects.all()
        tags = Tag.objects.all()
        questions = [Question(
            title=fake.sentence(nb_words=10)[:-1] + "?",
            text=fake.text(max_nb_chars=300),
            user=random.choice(users)) for _ in range(ratio * 10)]
        Question.objects.bulk_create(questions)
        for question in questions:
            tags_num = random.randint(1, 5)
            tags_list = random.SystemRandom().sample(list(tags), tags_num)
            for i in range(tags_num):
                question.tags.add(tags_list[i])
            question.save()
        print(f"{ratio * 10} questions finished.")

    def create_answers(self, ratio):
        questions = Question.objects.all()
        users = User.objects.all()
        answers = []
        for _ in range(ratio * 10):
            cur_question = random.choice(questions)
            answer = Answer(
                question=cur_question,
                user=random.choice(users),
                text=fake.text(max_nb_chars=300),
                status=random.choice([True, False]))
            answers.append(answer)
            cur_question.answers_count += 1
            cur_question.save()
        batch_size = 100
        count = 0
        cur_answers = list(answers)
        while count < ratio * 10:
            batch = list(islice(cur_answers, batch_size))
            cur_answers = cur_answers[batch_size:]
            count += batch_size
            Answer.objects.bulk_create(batch, batch_size)
        print(f"{ratio * 10} answers finished.")

    def create_likes(self, ratio):
        questions = Question.objects.all()
        answers = Answer.objects.all()
        users = User.objects.all()
        for _ in range(ratio * 200):
            random_choice = random.choice([0, 1])
            if random_choice:
                try:
                    cur_question = random.choice(questions)
                    like = QuestionLike(user=random.choice(users), question=cur_question)
                    cur_question.likes_count += 1
                    like.save()
                    cur_question.save()
                except IntegrityError:
                    continue
            else:
                try:
                    cur_answer = random.choice(answers)
                    like = AnswerLike(user=random.choice(users), answer=cur_answer)
                    cur_answer.likes_count += 1
                    like.save()
                    cur_answer.save()
                except IntegrityError:
                    continue
        print(f"{ratio * 200} likes finished.")
