from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^msrweb/', include('msrweb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^$', 'msrweb.anagram.views.main_index'),
    (r'^anagram/$', 'msrweb.anagram.views.anag_index'),
    (r'^anagram/(?P<word>\w+)/$', 'msrweb.anagram.views.anag_words'),
    (r'^anagram/(?P<word>\w+)/phrases$', 'msrweb.anagram.views.anag_phrases'),
)
