from django.conf.urls.defaults import *
from echo.models import Comment

info_dict = {
    'queryset':Comment.objects.all(),
}

urlpatterns = patterns('echo.views',
    (r'^$', 'index_view'),
    (r'^newComment/(?P<category>.*?)/(?P<comment>.*?)/$',   'newComment'),
    (r'^newComment/$',                                      'newComment'),
    (r'^newComment$',                                       'newComment'),
    (r'^postComment/$','postComment'),
    (r'^(?P<comment_id>\d+)/reply/$', 'reply'),
    (r'^(?P<category>\w+)/category/$','category'),
    (r'^logout/$','logout_view'),
    (r'^editComment/(?P<comment_id>\d+)/$','commentDetails'),
    (r'^search/', 'search'),
    (r'^ajax_search/', 'ajax_search'),
    (r'^register/$', 'registration'),
    (r'^voted/(?P<comment_id>\d+)/$', 'commentVote'),
)
