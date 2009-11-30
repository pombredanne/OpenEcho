from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import datetime


CATEGORIES = (
    ('IDEAS','Ideas'),
    ('QUESTIONS','Questions'),
    ('ISSUES','Issues'),
    ('PRAISE','Praise'),
)

class CategoryMeta(models.Model):
    category = models.CharField(max_length=10, choices=CATEGORIES)
    prompt = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.prompt[:50]

class Comment(models.Model):
    category = models.CharField(max_length=10, choices=CATEGORIES)
    commenter = models.ForeignKey(User)
    body = models.TextField("Comment text")
    votes = models.IntegerField("Votes",default=0)
    dstamp_created = models.DateTimeField("Date posted",auto_now_add=True)
    
    def __unicode__(self):
        return self.body[:75]
        
    def comment_summary(self):
        return self.body[:50] + "..."

class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    commenter = models.ForeignKey(User)
    body = models.TextField("Reply's text")
    dstamp_created = models.DateTimeField("Date posted",auto_now_add=True)
    
    def __unicode__(self):
        return self.body[:75]
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        
class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    company = models.CharField(max_length=100)
    max_votes = models.IntegerField("Maximum # of Votes",default=5)
        
