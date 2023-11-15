from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'How to build a moon park {i}',
        'content': f'Long Lorem ipsum {i}',
        'tags': ['blabla', 'alala']
    } for i in range(55)
]
QUESTIONS.append({
    'id': len(QUESTIONS),
    'title': 'How to build a moon park',
    'content': 'Long Lorem ipsum',
    'tags': ['blabla', 'lololo']
})

ANSWERS = [
    {
        'id': i,
        'content': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend, tortor id finibus feugiat, magna mauris gravida leo, et tincidunt nibh nisl et turpis. Sed consectetur ante vitae finibus finibus. Mauris at condimentum tellusac nisi nec sapien efficitur dapibus in ac sem. {i}'
    } for i in range(10)
]

MEMBERS = [
    {
        'id': 0,
        'name': 'Mr. Freeman'
    }, {
        'id': 1,
        'name': 'Dr. House'
    }, {
        'id': 2,
        'name': 'Queen Victoria'
    }
]

TAGS = [
    {
        'id': 0,
        'name': 'blabla'
    }, {
        'id': 1,
        'name': 'alala'
    }, {
        'id': 2,
        'name': 'lololo'
    }
]


def error_404_view(request, exception):
    return render(request, '404.html')


# per_page - how many ques on one page
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
    return render(request, 'index.html', {'tags': TAGS, 'members': MEMBERS, 'page_obj': paginate(request, QUESTIONS)})


def hot(request):
    return render(request, 'hot.html', {'tags': TAGS, 'members': MEMBERS, 'page_obj': paginate(request, QUESTIONS)})


def tag(request, tag):
    ques_obj = []
    for question in QUESTIONS:
        if tag in question['tags']:
            ques_obj.append(question)
    return render(request, 'tag.html',
                  {'tags': TAGS, 'members': MEMBERS, 'tag': tag, 'page_obj': paginate(request, ques_obj)})


def question(request, question_id):
    question = QUESTIONS[question_id]
    return render(request, 'question.html', {'tags': TAGS, 'members': MEMBERS, 'question': question,
                                             'page_obj': paginate(request, ANSWERS, 3)})


def login(request):
    return render(request, 'login.html', {'tags': TAGS, 'members': MEMBERS})


def signup(request):
    return render(request, 'signup.html', {'tags': TAGS, 'members': MEMBERS})


def ask(request):
    return render(request, 'ask.html', {'tags': TAGS, 'members': MEMBERS})


def settings(request):
    return render(request, 'settings.html', {'tags': TAGS, 'members': MEMBERS})
