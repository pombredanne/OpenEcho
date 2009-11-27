from settings import SITE_SRC_ROOT, os
from django import VERSION

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Uncomment the next line to enable the admin on Django-1.1:
    VERSION >= (1,1) and (r'^admin/', include(admin.site.urls)) or

    # Uncomment the next line to enable the admin on Django-1.0:
    (r'^admin/', admin.site.root),

    (r'^echo/', include('echo.urls')),
    (r'^$',include('echo.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name' : 'echo/login.html'}),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root' : os.path.join(SITE_SRC_ROOT, 'media')}),
)
