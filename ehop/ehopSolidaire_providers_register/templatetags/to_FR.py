# -*- coding: utf-8 -*-
# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - REZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django import template

register = template.Library()

@register.filter
def menu_to_FR(value):
    dict_to_FR = {'goalOfApplication': 'But de la demande',
                  'carringAgency': 'Structure d\'accompagnement',
                  'companies': 'Entreprises adhérentes',
                  'howKnowledge': 'Connaissance d\'Ehop',
                  'providerDeleteOptions': 'Offreur - Suppression de compte',
                  'applicantOptions0': 'Demandeur - Validation à 0',
                  'applicantOptions': 'Demandeur - Validation 1-99',
                  'applicantScheduleType': 'Demandeur - Type de planning'}
    return dict_to_FR.get(value, value)