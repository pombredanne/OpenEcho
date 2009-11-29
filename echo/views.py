# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from echo.models import Comment, Reply, CategoryMeta
from echo.forms import RegistrationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from haystack.query import SearchQuerySet
from django import forms
from voting.models import Vote

def index_view(request):
    faq_list = Comment.objects.filter(category='QUESTIONS')[:6]
    issue_list = Comment.objects.filter(category='ISSUES')[:6]
    idea_list = Comment.objects.filter(category='IDEAS')[:6]
    praise_list = Comment.objects.filter(category='PRAISE')[:6]
    return render_to_response('echo/index.html', {'faq_list':faq_list,
                                                  'issue_list':issue_list,
                                                  'idea_list':idea_list,
                                                  'praise_list':praise_list },
                              context_instance=RequestContext(request))


#user authentication and management...
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/echo')
    
def registration(request):
    f = RegistrationForm()
    
    if request.method == 'POST':
        f = RegistrationForm(request.POST)
        if f.is_valid():
            print "got validated registration entry...\n" 
            f.saveUnvalidatedUser()
            return HttpResponseRedirect('/echo/')
    else:
        f = RegistrationForm()
    
    return render_to_response("registration/register.html", {
                                  'form' : f },
                              context_instance=RequestContext(request))
    
    
@login_required
def newComment(request, category=None, comment=None):
    return render_to_response('echo/new_comment.html', {'category' : category,
                                                        'comment' : comment},
                               context_instance=RequestContext(request))
    
@login_required    
def postComment(request):
    c = Comment()
    c.body = request.POST['body']
    c.category = request.POST['category']
    u = request.user
    c.commenter = u
    c.save()
    return render_to_response('echo/edit_comment.html', {'comment' : c},
                              context_instance=RequestContext(request))

def commentDetails(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    r = c.reply_set.all()
    return render_to_response('echo/edit_comment.html', {'comment' : c,
                                                         'replies' : r},
                               context_instance=RequestContext(request))
        
@login_required    
def reply(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    r = Reply(comment=c,
              commenter=request.user,
              body=request.POST['body'])
    r.save()
    return render_to_response('echo/edit_comment.html', {'comment' : c,
                                                         'replies' : c.reply_set.all()},
                               context_instance=RequestContext(request))
    
def category(request, category):
    comment_list = Comment.objects.filter(category=category)
    return render_to_response('echo/category_list.html', { 'comments' : comment_list,
                                                           'category' : category},
                               context_instance=RequestContext(request))

def search(request):
    searchText = request.POST['search']
    return render_to_response('search/search.html', { 'results' : SearchQuerySet().auto_query(searchText),
                                                      'query' : searchText },
                               context_instance=RequestContext(request))
    
def ajax_search(request):
    search_text = request.POST['search_text']
    category    = request.POST['category']
    print "search_text = [" + search_text + "]\n"
    print "category = [" + category + "]\n"
    return render_to_response('search/ajax_search.html', { 'results' : SearchQuerySet().auto_query(search_text),
                                                           'query' : search_text,
                                                           'category' : category,
                                                         }  ,
                               context_instance=RequestContext(request))
                                                   
def commentVote(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    Vote.objects.record_vote(c,request.user,+1)
    return render_to_response('echo/record_vote.html', {}, context_instance=RequestContext(request))
