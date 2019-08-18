from django.shortcuts import render
import markdown
# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect
from .models import  ArticlePost
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
#import redirect
from django.core.paginator import Paginator
from comment.models import Comment
#from django.shortcuts import render, redirect
def article_list(request):
    # 修改变量名称（articles -> article_list）
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 4)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    context = { 'articles': articles, 'order': order }
    return render(request, 'article/list.html', context)

def article_detail(request,id):
    # get the article babe
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    # views +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # go to the templetes
    #lexer markdown
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    context = { 'article': article, 'toc': md.toc, 'comments': comments }
    return render(request, 'article/detail.html', context)
@login_required(login_url='/userprofile/login')
def article_create(request):
    # judge there is words?
    if request.method == 'POST':
        #submit the papers to chart

        article_post_form = ArticlePostForm(data = request.POST)
        if article_post_form.is_valid():
            #保存不提交
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id = request.user.id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("Invalid, please fill in again. ~~ 今日もいい日だっ~~")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)

def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    if request.user != article.author:
        return HttpResponse('You are not allowed to revise this blog.')
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")
# renew a article
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    #if http request is POST
    #using POST to change
    if request.user != article.author:
        return HttpResponse("You are not allowed to revise this blog.")
    if request.method =="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("invaild")
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)
