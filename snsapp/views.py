from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import SnsModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
from django.http.response import JsonResponse
from django.views import generic
from django.conf import settings
from newsapi import NewsApiClient

# Create your views here.

def signupfunc(request):
    #print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            #return render(request, 'login.html', {})
            return redirect('login')
        except IntegrityError:
            return render(request, 'signup.html', {'error':'このユーザーネームはすでに使用されています'})
    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
            #return render(request, 'login.html', {'context':'logged in'})
        else:
            return render(request, 'login.html', {'context':'not logged'})
    return render(request, 'login.html', {})

@login_required
def listfunc(request):
    object_list = SnsModel.objects.all()
    keyword = request.GET.get('keyword')
    if keyword:
        object_list = SnsModel.objects.filter(
            Q(title__icontains=keyword) | Q(author__icontains=keyword))
        #messages.success(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'list.html',{'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

@login_required
def detailfunc(request, pk):
    username = request.user
    object = get_object_or_404(SnsModel, pk=pk)
    return render(request, 'detail.html',{'object':object, 'user':username})

def goodfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect('list')

def apigoodfunc(request,pk):
    object = SnsModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    #return redirect('list')
    # ここまでは goodfuncと同じ
    return JsonResponse({"objectgood":object.good})

def readfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    username = request.user.get_username()
    login_user_id = request.user.id
    if username in object.readtext:
        return redirect('list')
    else:
        object.read = object.read + 1
        object.readtext = object.readtext + ' ' + username + str(login_user_id)
        object.save()
        return redirect('list')

class SnsCreate(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title', 'content', 'author', 'sns_image')
    success_url = reverse_lazy('list')

@require_POST
def deletefunc(request, pk):
    username = request.user
    user_author = SnsModel.objects.filter(author = username)
    #object_list = SnsModel.objects.all()
    object = get_object_or_404(user_author, pk=pk)
    object.delete()
    return redirect('list')

@login_required
def mylistfunc(request):
    username = request.user
    #ログインユーザーと一致するauthorのレコード件数を取得する
    user_author = SnsModel.objects.filter(author = username).count()
    #レコード件数が0以上はmyリストに表示
    if user_author > 0:
        object_list = SnsModel.objects.filter(author = username)
        return render(request, 'mylist.html',{'object_list':object_list})
    else:
        return render(request, 'mylist.html', {'context':'あなたの投稿はまだありません'})

def get_queryset(self):
    q_word = self.request.GET.get('query')
    if q_word:
        object_list = SnsModel.objects.filter(
            Q(title__icontains=q_word) | Q(author__icontains=q_word))
    return render(request, 'list.html',{'object_list':object_list})

#@method_decorator(login_required, name='get_context_data')
class SnsNews(generic.TemplateView):
    template_name = 'news.html'

    def get_context_data(self, **kwargs):
        context = super(SnsNews, self).get_context_data(**kwargs)
        newsapi = NewsApiClient(api_key=settings.NEWS_API)
        context['top_headlines'] = newsapi.get_top_headlines(category='entertainment')
        #print(context['top_headlines'])
        return context