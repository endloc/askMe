from django.shortcuts import render


# Create your views here.
# request - our HTTP-request
def index(request):
    questions = [
        {
            'id': i,
            'title': f'How to build a moon park {i}',
            'content': f'Long Lorem ipsum {i}'
        } for i in range(10)
    ]
    return render(request, 'index.html', {'questions': questions})


def question(request):
    return render(request, 'question.html')
