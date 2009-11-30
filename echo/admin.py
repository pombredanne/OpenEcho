#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Robert Neville on 2009-08-14.
Copyright (c) 2009 RetailArchitects. All rights reserved.
"""

from echo.models import Comment, Reply, CategoryMeta, UserProfile
from django.contrib import admin

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 2
    
class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    list_display = ('category','commenter','comment_summary')
    list_filter = ['dstamp_created','category','commenter']
    search_fields = ['body']
    date_hierarchy = 'dstamp_created'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category','prompt')

class ProfileAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Comment, CommentAdmin)
admin.site.register(CategoryMeta, CategoryAdmin)
admin.site.register(UserProfile, ProfileAdmin)
