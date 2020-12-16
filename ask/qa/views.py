from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from qa.models import Answer, Question
from django.http import HttpResponse
def test(request, *args, **kwargs):
    return HttpResponse('OK')

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page

@require_GET
def index(request):
    qs = Question.objects.all.new()
    paginator, page = paginate(request, qs)
    paginator.baseurl = reverse('index') + '?page='
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        })

@require_GET
def popular(request):
    qs = Question.objects.all.popular()
    paginator, page = paginate(request, qs)
    paginator.baseurl = reverse('popular') + '?page='
    return render(request, 'popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        })

@require_GET
def question_details(request, id):
    question = get_object_or_404(Question, id=id)
    answers = question.answer_set.all()
    return render(request, 'question_details.html', {
        'question': question,
        'answers': answers,
        })


