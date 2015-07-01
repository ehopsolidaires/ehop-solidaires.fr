# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django.conf.urls import patterns, url

urlpatterns = patterns('ehopSolidaire_providers_register.views',
                       url(r'^accueil/$', 'home', name='accueil'),
                       url(r'^offreur/$', 'formulaire', name='offreur'),
                       url(r'^fonctionnement/$', 'howwork', name='fonctionnement'),
                       url(r'^projet/$', 'project', name='projet'),
                       url(r'^demandeur/$','applicant', name='demandeur'),
                       url(r'^contact/$','contact', name='contact'),
                       url(r'^termine/$','submit', name='termine'),
                       url(r'^connexion/$','login_view', name='connexion'),
                       url(r'^mdp-oublie/$','forgotten', name='forgotten'),
                       url(r'^conditions/$', 'conditions', name='conditions'),
                       url(r'^validation-deconnexion/$', 'disconnected', name='deconnexion'),
                       url(r'^profil/$','profil', name='profil'),
                       url(r'^nouveau-mdp/$','change_password', name='change_password')
)
