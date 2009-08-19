from django.conf.urls.defaults import *
from feedback.echo.models import Comment

info_dict = {
    'queryset':Comment.objects.all(),
}

urlpatterns = patterns('feedback.echo.views',
    (r'^$', 'index_view'),
    (r'^newComment/$','newComment'),
    (r'^newComment$','newComment'),
    (r'^newComment/(?P<category>\w+)/','newComment'),
    (r'^postComment$','postComment'),
    (r'^(?P<comment_id>\d+)/reply/$', 'reply'),
    (r'^(?P<category>\w+)/category/$','category'),
    (r'^logout/$','logout_view'),
    (r'^editComment/(?P<comment_id>\d+)/$','commentDetails'),
    (r'^search/', 'search'),
)