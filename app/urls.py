from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]
