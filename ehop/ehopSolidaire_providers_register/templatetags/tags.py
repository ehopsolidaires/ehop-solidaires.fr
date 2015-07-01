# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - REZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django import template

register = template.Library()

@register.filter
def cleanAddress(value):
    new = value.replace(', France','').split(',')
    if new.__len__() > 1:
        return new[1]
    else:
        return new[0]