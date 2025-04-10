from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list':question_list} # 전달할 객체
    return render(request,'pybo/question_list.html', context)
    #return HttpResponse("안녕하세요 pybo에 오신걸 환영합니다.")

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                              create_date=timezone.now())
    # 등록 후 redirect로 상세페이지로 이동 localhost:8000/pybo/2/
    return redirect('pybo:detail', question_id=question.id)


def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
        else:
            return render(request, 'pybo/question_form.html', {'form': form})

    else:
        form = QuestionForm()
        return render(request, 'pybo/question_form.html', {'form':form})