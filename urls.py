from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from gabaluu.synopsis import views as synopsis_views
from gabaluu.account import views as account_views


import os.path

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

feeds = {
    'popular': synopsis_views.PopularFeed,
    'recent': synopsis_views.RecentFeed,
}


urlpatterns = patterns('',
    (r'^auth/$', account_views.auth),                   
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^login/$', auth_views.login, dict(template_name='login.html')),
    (r'^accounts/login/$', auth_views.login, dict(template_name='login.html')),
    (r'^logout/$', auth_views.logout, dict(next_page='/')),
    (r'^signup/$', account_views.signup),
    (r'^accounts/profile/$', account_views.profile),
    (r'^forgot/password/$', auth_views.password_reset),
    (r'^forgot/password/done/$', auth_views.password_reset_done),
    (r'^password/change/$', auth_views.password_change),
    (r'^password/change/done/$', auth_views.password_change_done),
    (r'^$', synopsis_views.index),
    (r'^popular/$', synopsis_views.popular),
    (r'^popular/(?P<current_page>\w+)/$', synopsis_views.popular),
    (r'^recent/$', synopsis_views.recent),
    (r'^recent/(?P<current_page>\w+)/$', synopsis_views.recent),
    (r'^tags/(?P<tag>\w+)/$', synopsis_views.tagged),
    (r'^tags/(?P<tag>\w+)/(?P<current_page>\w+)/$', synopsis_views.tagged),
    (r'^sites/(?P<site>\w+)/$', synopsis_views.sites),
    (r'^search/$', synopsis_views.synopsis_search),
    (r'^members/$', account_views.members),
    (r'^terms/$', synopsis_views.terms),
    (r'^privacy/$', synopsis_views.privacy),
    (r'^about/$', synopsis_views.about),
    (r'^profile/(?P<username>\w+)/$', account_views.user_profile_posted),
    (r'^profile/(?P<username>\w+)/voted/$', account_views.user_profile_voted),
    (r'^profile/(?P<username>\w+)/commented/$', account_views.user_profile_commented),    
    (r'^synopsis/(?P<synopsis_id>\w+)/vote/$', synopsis_views.synopsis_vote),
    (r'^synopsis/new/$', synopsis_views.synopsis_new),
    (r'^synopsis/(?P<permalink>\w+)/edit/$', synopsis_views.synopsis_edit),
    (r'^synopsis/(?P<permalink>\w+)/$', synopsis_views.synopsis_detail),
    (r'^synopsis/(?P<synopsis_id>\w+)/comments/create/$', synopsis_views.comment_create),
    (r'^synopsis/(?P<synopsis_id>\w+)/comments/(?P<comment_id>\w+)/create/$', synopsis_views.comment_create),
    (r'^synopsis/(?P<synopsis_id>\w+)/link/$', synopsis_views.synopsis_link),
    (r'^synopsis/(?P<permalink>\w+)/preview/$', synopsis_views.synopsis_preview),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds})
)

# Use Django to serve media files only during development.
# Settings.py for Production: DEBUG = FALSE
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                             dict(document_root=os.path.join(PROJECT_PATH, 'media'))),
    )
                            
