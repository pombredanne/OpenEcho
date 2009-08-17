# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from feedback.echo.models import Comment, Reply, CategoryMeta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index_view(request):
    faq_list = Comment.objects.filter(category='QUESTIONS')[:3]
    issue_list = Comment.objects.filter(category='ISSUES')[:3]
    idea_list = Comment.objects.filter(category='IDEAS')[:3]
    praise_list = Comment.objects.filter(category='PRAISE')[:3]
    return render_to_response('echo/index.html', {'faq_list':faq_list,
                                                  'issue_list':issue_list,
                                                  'idea_list':idea_list,
                                                  'praise_list':praise_list })

@login_required
def newComment(request, category=None):
    return render_to_response('echo/new_comment.html', {'category':category})
    
@login_required    
def postComment(request):
    c = Comment()
    c.body = request.POST['body']
    c.category = request.POST['category']
    u = request.user
    c.commenter = u
    c.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def commentDetails(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    r = c.reply_set.all()
    return render_to_response('echo/edit_comment.html', {'comment' : c,
                                                         'replies' : r})
        
@login_required    
def reply(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    r = Reply(comment=c,
              commenter=request.user,
              body=request.POST['body'])
    r.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
@login_required
def category(request, category):
    comment_list = Comment.objects.filter(category=category)
    return render_to_response('echo/category_list.html', { 'comments' : comment_list,
                                                           'category' : category})

def search(request):
    searchText = request.POST['search']
    category = request.POST['category']
    
                                                           
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/echo')
    