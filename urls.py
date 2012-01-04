from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin, databrowse
import info

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pilot.views.home', name='home'),
    # url(r'^pilot/', include('pilot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/info/companysponsoredcontractinfo/', 'info.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
