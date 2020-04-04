from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from polls.models import Question, Choice
from django.template import loader

"""
def index(request):
   '''
    #首次进入Django的
    return HttpResponse("Hello, world. You're at the polls index.")
   '''
    '''
    #配置问题搜索的
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    output = ','.join([q.question_text for q in latest_question_list])
    HttpResponse(output)
    '''
    # 配置引擎模板，配合template一起使用
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template("polls/index.html")
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    # return HttpResponse("You are looking at question %s." % question_id)
    '''
    #常规代码
     try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    '''
    # 偷懒方式
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    '''
     response = "You are Looking at the result of question %s."
    return HttpResponse(response % question_id)
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""


# 修改后的视图
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
