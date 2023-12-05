from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer, Tag, User


# TODO: COMENT WHEN MIGRATE
TAGS = list(Tag.objects.all())
TAGS = TAGS[:10]
USERS = list(User.objects.all())
USERS = USERS[:5]


def error_404_view(request, exception):
    return render(request, '404.html')


def paginate(request, objects, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    try:
        int_page_number = int(page_number)
        if int_page_number <= 0:
            page_number = 1
        elif int_page_number > paginator.num_pages:
            page_number = paginator.num_pages
        else:
            page_number = int_page_number
    except ValueError:
        page_number = 1
    except TypeError:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    new_questions = list(Question.objects.new_questions())
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    print(USERS)
    return render(request, "index.html",
                  {'tags': TAGS, 'members': USERS, 'page_obj': paginate(request, new_questions)})
    # return render(request, 'index.html', {'tags': TAGS, 'members': MEMBERS, 'page_obj': paginate(request, QUESTIONS)})


def hot(request):
    hot_questions = list(Question.objects.hot_questions())
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, "hot.html",
                  {'tags': TAGS, 'members': USERS, 'page_obj': paginate(request, hot_questions)})
    # return render(request, 'hot.html', {'tags': TAGS, 'members': MEMBERS, 'page_obj': paginate(request, QUESTIONS)})


def by_tag(request, tag_name):
    tag = Tag.objects.tag_by_name(tag_name)
    questions = list(Question.objects.questions_by_tag(tag))
    return render(request, "tag.html",
                  {'tags': TAGS, 'members': USERS, 'tag': tag,
                   'page_obj': paginate(request, questions)})


def question(request, question_id):
    question = Question.objects.question_by_id(question_id)
    answers = list(Answer.objects.answers_by_question(question))
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, 'question.html', {'tags': TAGS, 'members': USERS,
                                             'question': question, 'page_obj': paginate(request, answers, 3)})


def login(request):
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, 'login.html',
                  {'tags': TAGS, 'members': USERS})


def signup(request):
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, 'signup.html',
                  {'tags': TAGS, 'members': USERS})


def ask(request):
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, 'ask.html',
                  {'tags': TAGS, 'members': USERS})


def settings(request):
    # tags = list(Tag.objects.all())
    # users = list(User.objects.all())
    return render(request, 'settings.html',
                  {'tags': TAGS, 'users': USERS})
