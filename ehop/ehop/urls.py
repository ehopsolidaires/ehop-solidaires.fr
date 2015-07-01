# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django.conf.urls import *
from django.http import *
# from django.contrib.sitemaps.views import sitemap
# Uncomment the next two lines to enable the admin:
from django.contrib import admin



  # Examples:
    # url(r'^$', 'ehop.views.home', name='home'),
    # url(r'^ehop/', include('ehop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


urlpatterns = patterns('',
                       url(r'^$', 'ehopSolidaire_providers_register.views.home'),
                       url(r'^', include('ehopSolidaire_providers_register.urls')),
                       url(r'^', include('admin.urls')),
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^google8882ba66ac2c6fa9\.html$', lambda r: HttpResponse("google-site-verification: google8882ba66ac2c6fa9.html", content_type="text/plain")),
                       url(r'^sitemap\.xml$', 'ehopSolidaire_providers_register.views.sitemap')
                       # url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
)
