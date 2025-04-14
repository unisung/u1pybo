from tkinter.font import names

from django.urls import path

from . import views

app_name = 'pybo' # namespace 추가

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/',views.detail, name='detail'),
    path('answer/create/<int:question_id>',views.answer_create,name="answer_create"),
    path('question/create/',views.question_create,name="question_create"),
    path('question/modify/<int:question_id>/',views.question_modify,name="question_modfy")
]
