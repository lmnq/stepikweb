from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from qa.models import Answer, Question
from qa.forms import AskForm, AnswerForm, SignupForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
    qs = Question.objects.all().order_by('-id')
    paginator, page = paginate(request, qs)
    paginator.baseurl = reverse('index') + '?page='
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        })

@require_GET
def popular(request):
    qs = Question.objects.all().order_by('-rating')
    paginator, page = paginate(request, qs)
    paginator.baseurl = reverse('popular') + '?page='
    return render(request, 'popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        })

def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
	    form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask_form.html', {
        'form': form,
	'user': request.user,
	'session': request.session,
        })

def question_details(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method =="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
	    form._user = request.user
            answer = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request, 'question_details.html', {
        'question': question,
        'form': form,
	'user': request.user,
	'session': request.session,
        })

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.raw_passeord
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form,
                                           'user': request.user,
                                           'session': request.session, })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(username, password)
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'user': request.user,
                                          'session': request.session, })
