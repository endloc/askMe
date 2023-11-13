from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'How to build a moon park {i}',
        'content': f'Long Lorem ipsum {i}'
    } for i in range(55)
]


# per_page - how many ques on one page
def paginate(request, objects, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    # page = request.GET.get('page', 1)
    return render(request, 'index.html', {'page_objects': paginate(request, QUESTIONS)})


def hot(request):
    # page = request.GET.get('page', 1)
    return render(request, 'hot.html', {'page_objects': paginate(request, QUESTIONS)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
