from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page','1')  # 페이지값이 있으면 해당페이지로, 없으면1 페이지
    # 조회
    question_list = Question.objects.order_by('-create_date')
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 조회한결과 페이지당 10개씪 보이기
    page_obj = paginator.get_page(page) # 조회결과를 한페이지당나눠서 페이지객체로 재생성

    # context = {'question_list':question_list} # 전달할 객체
    context = {'question_list':page_obj}
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

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user #추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()

    return render(request, 'pybo/question_detail.html',
                  {'question': question, 'form':form})

    #
    # question.answer_set.create(content=request.POST.get('content'),
    #                           create_date=timezone.now())
    # # 등록 후 redirect로 상세페이지로 이동 localhost:8000/pybo/2/
    # return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        form = QuestionForm()

    return render(request, 'pybo/question_form.html', {'form':form})