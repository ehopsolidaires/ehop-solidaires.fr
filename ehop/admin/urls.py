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
urlpatterns = patterns('admin.views',
                       url(r'^BO/$','bo', name='bo'),
                       url(r'^BO/utilisateurs/$', 'users'),
                       url(r'^BO/sort/$', 'search_order'),
                       url(r'^BO/ajout_demandeur/$', 'add_applicant', name='applicant'),
                       url(r'^BO/utilisateurs/d/(?P<applicant_id>\d+)/$', 'applicant', name='bo'),
                       url(r'^BO/utilisateurs/o/(?P<provider_id>\d+)/$', 'provider', name='bo'),
                       url(r'^BO/recherche/(?P<calendar_id>\d+)/$', 'research', name='research'),
                       url(r'^BO/utilisateurs/d/recherches/(?P<calendar_id>\d+)/$', 'applicant_search', name='bo'),
                       url(r'^BO/utilisateurs/d/calendrier/(?P<applicant_id>\d+)/$', 'add_calendar', name='bo'),
                       url(r'^BO/utilisateurs/d/calendrier/mod/(?P<calendar_id>\d+)/$', 'modify_calendar', name='bo'),
                       url(r'^BO/sms/(?P<provider_id>\d+)/(?P<calendar_id>\d+)/$','sms'),
                       url(r'^BO/sms/$', 'sms_new', name='sms_new'),
                       url(r'^BO/generate_chart/(?P<id>\d+)/(?P<dates>\w+)/(?P<params>\w+)/$','generate_chart'),
                       url(r'^BO/generate_csv/(?P<id>\d+)/$','generate_csv'),
                       url(r'^BO/generate_csv/(?P<id>\d+)/(?P<dates>\w+)/$','generate_csv'),
                       url(r'^BO/generate_csv/(?P<id>\d+)/(?P<dates>\w+)/(?P<params>\w+)/$','generate_csv'),
                       url(r'^BO/stats','stats', name='stats'),
                       url(r'^BO/parametrages','settings', name='settings')
)
