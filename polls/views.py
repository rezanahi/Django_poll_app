from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question
from django.template import loader


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, template_name="polls/index.html", context=context)


def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, template_name='polls/detail.html', context={"question": q})


def result(request, question_id):
    return HttpResponse(f"You are looking at the results of question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"You are voting on question {question_id}")


