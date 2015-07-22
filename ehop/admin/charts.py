# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date

import django.core as core
from ehopSolidaire_providers_register.models import *
from django.db.models import Count
from django.db.models import Q
from django.db import connection
import time
import operator


class ChartData(object):
    ''' CHARTS '''
    @classmethod
    def get_provider_date_register(cls, per, intercom, dept, start_date, end_date):
        if per == 'day' or per == 'week':
            format = 'DD/MM/YYYY'
            py_format = '%d/%m/%Y'
        elif per == 'month':
            format = 'MM/YYYY'
            py_format = '%m/%Y'
        else:
            format = 'YYYY'
            py_format = '%Y'
        providers = Provider.objects.all().values_list('idUser', flat=True)
        extra_query = 'to_char(public."ehopSolidaire_providers_register_user"."dateRegister",\''+format+'\')'
        print dept
        if intercom != "all":
            timer_start = time.time()
            providers = User.objects.filter(idUser__in=providers).select_related('idHomeAddress')
            intercoms = get_intercommunities()
            user_intercom = [u.idUser for u in providers if sameIntercommunity(u.idHomeAddress.street, intercom, intercoms)]
            if start_date == "0" and end_date == "0":
                user_register = User.objects.filter(Q(idUser__in=user_intercom)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeIntercommunity=intercom) & Q(homeZipCode__startswith=dept)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            elif start_date == "0":
                user_register = User.objects.filter(Q(idUser__in=user_intercom) & Q(dateRegister__lte=end_date) & Q(zipCode__startswith=dept)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeIntercommunity=intercom) & Q(dateRegister__lte=end_date)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            elif end_date == "0":
                user_register = User.objects.filter(Q(idUser__in=user_intercom) & Q(dateRegister__gte=start_date)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeIntercommunity=intercom) & Q(dateRegister__gte=start_date)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            else:
                user_register = User.objects.filter(Q(idUser__in=user_intercom) & Q(dateRegister__range=[start_date,end_date])).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeIntercommunity=intercom) & Q(dateRegister__range=[start_date,end_date])).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            print time.time() - timer_start
        else:
            if start_date == "0" and end_date == "0":
                user_register = User.objects.filter(Q(idUser__in=providers) & Q(zipCode__startswith=dept)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeZipCode__startswith=dept)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            elif start_date == "0":
                user_register = User.objects.filter(Q(idUser__in=providers) & Q(zipCode__startswith=dept) & Q(dateRegister__lte=end_date)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeZipCode__startswith=dept) & Q(dateRegister__lte=end_date)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            elif end_date == "0":
                user_register = User.objects.filter(Q(idUser__in=providers) & Q(zipCode__startswith=dept) & Q(dateRegister__gte=start_date)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeZipCode__startswith=dept) & Q(dateRegister__gte=start_date)).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
            else:
                user_register = User.objects.filter(Q(idUser__in=providers) & Q(zipCode__startswith=dept) & Q(dateRegister__range=[start_date,end_date])).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
                extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateRegister",\''+format+'\')'
                user_deleted_register = Deletion.objects.filter(Q(type="provider") & Q(homeZipCode__startswith=dept) & Q(dateRegister__range=[start_date,end_date])).order_by('dateRegister')\
                    .extra({'dateR':extra_query}).values('dateR').annotate(nb=Count('id'))
        return get_data_user_register(list(user_register)+list(user_deleted_register), weeks=per == 'week', start=start_date, end=end_date, format=py_format)

    @classmethod
    def get_provider_total_registered(cls, per, intercom, dept, start_date, end_date):
        if per == 'day' or per == 'week':
            format = 'DD/MM/YYYY'
            py_format = '%d/%m/%Y'
        elif per == 'month':
            format = 'MM/YYYY'
            py_format = '%m/%Y'
        else:
            format = 'YYYY'
            py_format = '%Y'
        providers = Provider.objects.all().values_list('idUser', flat=True)
        extra_query = 'to_char(public."ehopSolidaire_providers_register_user"."dateRegister",\''+format+'\')'
        if intercom != "all":
            providers = User.objects.filter(idUser__in=providers).select_related('idHomeAddress')
            intercoms = get_intercommunities()
            user_intercom = [u.idUser for u in providers if sameIntercommunity(u.idHomeAddress.street, intercom, intercoms)]
            user_register = User.objects.filter(idUser__in=user_intercom).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))

        else:
            user_register = User.objects.filter(Q(idUser__in=providers) & Q(zipCode__startswith=dept)).order_by('dateRegister').extra({'dateR':extra_query})\
                    .values('dateR').annotate(nb=Count('idUser'))
        return get_data_user_register(user_register, total=True, weeks=per == 'week', start=start_date, end=end_date, format=py_format)

    @classmethod
    def get_chart_unsubs(cls, per, intercom, dept, start_date, end_date):
        if per == 'day' or per == 'week':
            format = 'DD/MM/YYYY'
            py_format = '%d/%m/%Y'
        elif per == 'month':
            format = 'MM/YYYY'
            py_format = '%m/%Y'
        else:
            format = 'YYYY'
            py_format = '%Y'
        extra_query = 'to_char(public."ehopSolidaire_providers_register_deletion"."dateDelete",\''+format+'\')'
        if intercom != "all":
            user_delete = Deletion.objects.filter(Q(homeIntercommunity=intercom)).order_by('dateDelete').extra({'dateR':extra_query})\
                .values('dateR').annotate(nb=Count('id'))
        else:
            user_delete = Deletion.objects.filter(homeZipCode__startswith=dept).order_by('dateDelete').extra({'dateR':extra_query})\
                .values('dateR').annotate(nb=Count('id'))
        return get_data_user_register(user_delete, weeks=per == 'week', start=start_date, end=end_date, format=py_format)

    @classmethod
    def get_counters_provider_applicant(cls, intercom, dept, start_date, end_date):
        if intercom != "all":
            if start_date == "0" and end_date == "0":
                users = User.objects.all()
            elif start_date == "0":
                users = User.objects.filter(dateRegister__lte=end_date)
            elif end_date == "0":
                users = User.objects.filter(dateRegister__gte=start_date)
            else:
                users = User.objects.filter(dateRegister__range=[start_date, end_date])
            intercoms = get_intercommunities()
            user_intercom = [u.idUser for u in users if sameIntercommunity(u.idHomeAddress.street, intercom, intercoms)]
            providers = Provider.objects.filter(idUser__idUser__in=user_intercom).count()
            applicants = Applicant.objects.filter(idUser__idUser__in=user_intercom).count()
        else:
            if start_date == "0" and end_date == "0":
                providers = Provider.objects.all()
                applicants = Applicant.objects.all()
            elif start_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__lte=end_date)
                applicants = Applicant.objects.filter(idUser__dateRegister__lte=end_date)
            elif end_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__gte=start_date)
                applicants = Applicant.objects.filter(idUser__dateRegister__gte=start_date)
            else:
                providers = Provider.objects.filter(idUser__dateRegister__range=[start_date, end_date])
                applicants = Applicant.objects.filter(idUser__dateRegister__range=[start_date, end_date])
            providers = providers.filter(idUser__zipCode__startswith=dept).count()
            applicants = applicants.filter(idUser__zipCode__startswith=dept).count()
        return {'providers':providers, 'applicants':applicants}

    @classmethod
    def get_chart_provider_origins(cls, param, start_date='0', end_date='0'):
        if param == "firm" or param == "adfirm":
            if start_date == "0" and end_date == "0":
                providers = Provider.objects.all().values('company')
            elif start_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__lte=end_date).values('company')
            elif end_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__gte=start_date).values('company')
            else:
                providers = Provider.objects.filter(idUser__dateRegister__range=[start_date, end_date]).values('company')
        if param == "firm":
            firms = Companies.objects.all().values_list('name', flat=True)
            data = {firm.encode('utf-8'):0 for firm in firms}
            for provider in providers:
                if provider['company'] != None:
                    if provider['company'].encode('utf-8') not in data.keys():
                        data[provider['company'].encode('utf-8')] = 1
                    else:
                        data[provider['company'].encode('utf-8')] += 1
        if param == "adfirm":
            firms = Companies.objects.all().values_list('name', flat=True)
            data = {firm.encode('utf-8'):0 for firm in firms}
            for provider in providers:
                if provider['company'] == None:
                    provider['company'] = u''
                if provider['company'].encode('utf-8') in data.keys():
                    data[provider['company'].encode('utf-8')] += 1
        if param == "COMCOM":
            intercommunities = Intercommunity.objects.values_list('intercommunity', flat=True)
            data = {intercommunity:0 for intercommunity in intercommunities}
            if start_date == "0" and end_date == "0":
                providers = Provider.objects.all().values('idUser__idHomeAddress__street')
            elif start_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__lte=end_date).values('idUser__idHomeAddress__street')
            elif end_date == "0":
                providers = Provider.objects.filter(idUser__dateRegister__gte=start_date).values('idUser__idHomeAddress__street')
            else:
                providers = Provider.objects.filter(idUser__dateRegister__range=[start_date, end_date]).values('idUser__idHomeAddress__street')
            intercoms = get_intercommunities()
            for provider in providers:
                comcom = get_intercommunity(intercoms, provider['idUser__idHomeAddress__street'].replace(', France',''))
                if comcom != "":
                    data[comcom] += 1
        return sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    ''' CSV EXPORT '''
    @classmethod
    def get_all_providers_info(cls,start_date, end_date, params):
        if start_date != "0":
            start = datetime.strptime(start_date,'%d%m%Y')
        if end_date != "0":
            end = datetime.strptime(end_date,'%d%m%Y') + timedelta(days=1)
        if start_date == "0" and end_date == "0":
            providers = Provider.objects.all().select_related()
        elif start_date == "0":
            providers = Provider.objects.filter(idUser__dateRegister__lte=end).select_related()
        elif end_date == "0":
            providers = Provider.objects.filter(idUser__dateRegister__gte=start).select_related()
        else:
            providers = Provider.objects.filter(idUser__dateRegister__range=[start, end]).select_related()
        data = generate_providers_headers(params)
        intercommunities = get_intercommunities()
        for i, provider in enumerate(providers):
            data.append([])
            data = generate_providers_row(data, i+1, provider, params, intercommunities)
        return data


    @classmethod
    def get_all_applicants_info(cls, start_date, end_date, params):
        if start_date != "0":
            start = datetime.strptime(start_date,'%d%m%Y')
        if end_date != "0":
            end = datetime.strptime(end_date,'%d%m%Y') + timedelta(days=1)
        if start_date == "0" and end_date == "0":
            calendars = HistoricCalendar.objects.all().select_related()
        elif start_date == "0":
            calendars = HistoricCalendar.objects.filter(idApplicant__idUser__dateRegister__lte=end).select_related()
        elif end_date == "0":
            calendars = HistoricCalendar.objects.filter(idApplicant__idUser__dateRegister__gte=start).select_related()
        else:
            calendars = HistoricCalendar.objects.filter(idApplicant__idUser__dateRegister__range=[start, end]).select_related()
        data = generate_applicants_headers(params)
        intercommunities = get_intercommunities()
        calendars, index_of = create_calendars_list(calendars)
        previous_calendar = None
        row_count = 1
        for calendar in calendars:
            data.append([])
            data, n = generate_applicants_row(data, row_count, calendar, params, intercommunities, previous_calendar, index_of)
            row_count += n
            previous_calendar = calendar
        return data

    @classmethod
    def get_car_sharings(cls, start_date, end_date):
        if start_date != "0":
            start = datetime.strptime(start_date, '%d%m%Y')
        if end_date != "0":
            end = datetime.strptime(end_date, '%d%m%Y') + timedelta(days=1)
        if start_date == "0" and end_date == "0":
            car_sharings = Historic.objects.all().select_related()
        elif start_date == "0":
            car_sharings = Historic.objects.filter(date__lte=end).select_related()
        elif end_date == "0":
            car_sharings = Historic.objects.filter(date__gte=start).select_related()
        else:
            car_sharings = Historic.objects.filter(date__range=[start, end]).select_related()
        data = generate_car_sharings_headers()
        intercommunities = get_intercommunities()
        for car_share in car_sharings:
            data.append(generate_car_sharings_row(car_share, intercommunities))
        return data

    @classmethod
    def get_unsubs(cls, start_date, end_date):
        if start_date != "0":
            start = datetime.strptime(start_date,'%d%m%Y')
        if end_date != "0":
            end = datetime.strptime(end_date,'%d%m%Y') + timedelta(days=1)
        if start_date == "0" and end_date == "0":
            unsubs = Deletion.objects.all().select_related()
        elif start_date == "0":
            unsubs = Deletion.objects.filter(dateDelete__lte=end).select_related()
        elif end_date == "0":
            unsubs = Deletion.objects.filter(dateDelete__gte=start).select_related()
        else:
            unsubs = Deletion.objects.filter(dateDelete__range=[start, end]).select_related()
        data = generate_unsubs_headers()
        for unsub in unsubs:
            data.append(generate_unsubs_row(unsub))
        return data


def generate_unsubs_headers():
    data = list()
    data.append(u'id')
    data.append(u'Date de suppression')
    data.append(u'Date d\'inscription')
    data.append(u'Raison')
    data.append(u'Domicile')
    data.append(u'Département Domicile'.encode('latin-1'))
    data.append(u'Travail')
    return [data]


def generate_unsubs_row(unsub):
    data = list()
    data.append(unsub.pk)
    data.append(unsub.dateDelete.strftime('%d/%m/%Y'))
    data.append(unsub.dateRegister.strftime('%d/%m/%Y'))
    data.append(unsub.reason.encode("latin-1"))
    data.append(unsub.homeIntercommunity.encode("latin-1"))
    data.append(get_departement(unsub.homeZipCode))
    data.append(unsub.workIntercommunity.encode("latin-1"))
    return data


def generate_car_sharings_headers():
    data = list()
    data.append(u'id')
    data.append(u'Date du covoiturage')
    data.append(u'Prénom (offreur)'.encode("latin-1"))
    data.append(u'Nom (offreur)')
    data.append(u'Prénom (demandeur)'.encode("latin-1"))
    data.append(u'Nom (demandeur)')
    data.append(u'Départ'.encode("latin-1"))
    data.append(u'Départ COMCOM'.encode("latin-1"))
    data.append(u'Départ département'.encode("latin-1"))
    data.append(u'Arrivée'.encode("latin-1"))
    data.append(u'Arrivée COMCOM'.encode("latin-1"))
    data.append(u'Détour (temps)'.encode("latin-1"))
    data.append(u'Détour (distance)'.encode("latin-1"))
    return [data]




def generate_car_sharings_row(car_share, intercommunities):
    data = list()
    data.append(car_share.idHistoric)
    data.append(car_share.date.strftime('%d/%m/%Y'))
    data.append(car_share.idPath.idProvider.idUser.firstname.encode("latin-1"))
    data.append(car_share.idPath.idProvider.idUser.name.encode("latin-1"))
    data.append(car_share.idHistoricCalendar.idApplicant.idUser.firstname.encode("latin-1"))
    data.append(car_share.idHistoricCalendar.idApplicant.idUser.name.encode("latin-1"))
    data.append(car_share.streetDeparture.encode("latin-1"))
    data.append(get_intercommunity(intercommunities,car_share.streetDeparture).encode("latin-1"))
    data.append(get_departement(car_share.idHistoricCalendar.idApplicant.idUser.zipCode))
    data.append(car_share.streetArrival.encode("latin-1"))
    data.append(get_intercommunity(intercommunities,car_share.streetArrival).encode("latin-1"))
    data.append(car_share.detour)
    data.append(car_share.detourkm)
    return data



def create_calendars_list(calendars):
    cals = list()
    index_of = {'idApplicant': 0, 'dateRegister': 1, 'firstname': 2, 'name': 3, 'yearOfBirth': 4, 'sex': 5, 'mail': 6,
                'phone': 7, 'carringAgency': 8, 'goalOfApplication': 9, 'scheduleType': 10, 'transportIssue': 11,
                'success': 12, 'comment': 13, 'dateBeginning': 14, 'selectedDays': 15, 'intervalDays': 16, 'streetHome': 17,
                'homeDept':18, 'streetWork': 19, 'firstWeek': 20, 'lastWeek': 21}
    for calendar in calendars:
        data = list()
        data.append(calendar.idApplicant.idApplicant)
        data.append(calendar.idApplicant.idUser.dateRegister)
        data.append(calendar.idApplicant.idUser.firstname.encode('latin-1'))
        data.append(calendar.idApplicant.idUser.name.encode('latin-1'))
        data.append(calendar.idApplicant.yearOfBirth)
        data.append(calendar.idApplicant.idUser.sex)
        data.append(calendar.idApplicant.idUser.get_mail().encode('latin-1'))
        data.append(calendar.idApplicant.idUser.phone.encode('latin-1'))
        data.append(calendar.idApplicant.get_carringAgency().encode('latin-1'))
        data.append(calendar.idApplicant.get_goalOfApplication().encode('latin-1'))
        data.append(calendar.idApplicant.scheduleType.encode('latin-1'))
        data.append(calendar.get_transportIssue().encode('latin-1'))
        data.append(calendar.pourcentage)
        data.append(calendar.get_comment().encode('latin-1'))
        data.append(calendar.dateBeginning)
        data.append(calendar.get_numberof_selected_days())
        data.append(calendar.get_interval_days())
        data.append(calendar.idApplicant.idUser.idHomeAddress.get_cleaned_street())
        data.append(get_departement(calendar.idApplicant.idUser.zipCode))
        data.append(calendar.idApplicant.idUser.idWorkAddress.get_cleaned_street())
        data.append(calendar.get_first_week_number())
        data.append(calendar.get_last_week_number())
        cals.append(data)
    cals.sort(key=lambda x: (x[index_of['idApplicant']], x[index_of['dateBeginning']]))
    return cals, index_of


def generate_providers_headers(params):
    idProvider = 'idProvider' not in params
    dateRegister = 'dateRegister' not in params
    firstname = 'firstname' not in params
    name = 'name' not in params
    sex = 'sex' not in params
    mail = 'mail' not in params
    phone = 'phone' not in params
    company = 'company' not in params
    howKnowledge = 'howKnowledge' not in params
    homeAddress = 'homeAddress' not in params
    homeIntercommunity = 'homeIntercommunity' not in params
    homeDept = 'homeDept' not in params
    workAddress = 'workAddress' not in params
    workIntercommunity = 'workIntercommunity' not in params
    planningType = 'planningType' not in params
    data = []
    if idProvider:
        data.append('id')
    if dateRegister:
        data.append('Date d\'Inscription')
    if firstname:
        data.append(u'Prénom'.encode('latin-1'))
    if name:
        data.append('Nom')
    if sex:
        data.append('Sexe')
    if mail:
        data.append('Mail')
    if phone:
        data.append(u'Téléphone'.encode('latin-1'))
    if company:
        data.append('Entreprise')
    if howKnowledge:
        data.append('Connaissance d\'Ehop Solidaires')
    if homeAddress:
        data.append('Adresse du Domicile')
    if homeIntercommunity:
        data.append(u'Communauté de commune (Domicile)'.encode('latin-1'))
    if homeDept:
        data.append(u'Départ département'.encode("latin-1"))
    if workAddress:
        data.append('Adresse du travail')
    if workIntercommunity:
        data.append(u'Communauté de commune (Travail)'.encode('latin-1'))
    if planningType:
        data.append('Type de planning')
    return [data]


def generate_providers_row(data, i, provider, params, intercommunities):
    idProvider = 'idProvider' not in params
    dateRegister = 'dateRegister' not in params
    firstname = 'firstname' not in params
    name = 'name' not in params
    sex = 'sex' not in params
    mail = 'mail' not in params
    phone = 'phone' not in params
    company = 'company' not in params
    howKnowledge = 'howKnowledge' not in params
    homeAddress = 'homeAddress' not in params
    homeIntercommunity = 'homeIntercommunity' not in params
    homeDept = 'homeDept' not in params
    workAddress = 'workAddress' not in params
    workIntercommunity = 'workIntercommunity' not in params
    planningType = 'planningType' not in params
    if idProvider:
        data[i].append(provider.idProvider)
    if dateRegister:
        data[i].append(provider.idUser.dateRegister.date().strftime('%d/%m/%Y'))
    if firstname:
        data[i].append(provider.idUser.firstname.encode('latin-1'))
    if name:
        data[i].append(provider.idUser.name.encode('latin-1'))
    if sex:
        data[i].append(provider.idUser.sex)
    if mail:
        data[i].append(provider.idUser.get_mail().encode('latin-1'))
    if phone:
        data[i].append(provider.idUser.phone.encode('latin-1'))
    if company:
        if provider.company:
            data[i].append(provider.company.encode('latin-1'))
        else:
            data[i].append('')
    if howKnowledge:
        data[i].append(provider.howKnowledge.encode('latin-1'))
    if homeAddress:
        data[i].append(provider.idUser.idHomeAddress.get_cleaned_street().encode('latin-1'))
    if homeIntercommunity:
        address = provider.idUser.idHomeAddress.street
        data[i].append(get_intercommunity(intercommunities, address))
    if homeDept:
        data[i].append(get_departement(provider.idUser.zipCode))
    if workAddress:
        data[i].append(provider.idUser.idWorkAddress.get_cleaned_street().encode('latin-1'))
    if workIntercommunity:
        address = provider.idUser.idWorkAddress.street
        data[i].append(get_intercommunity(intercommunities, address))
    if planningType:
        paths = Path.objects.filter(idProvider=provider.idProvider)
        if paths:
            planning_type = paths[0].getPlanningType()
        else:
            planning_type = "Inconnu"
        data[i].append(planning_type)
    return data


def generate_applicants_headers(params):
    idCalendar = 'idCalendar' not in params
    dateRegister = 'dateRegister' not in params
    firstname = 'firstname' not in params
    name = 'name' not in params
    yearOfBirth = 'yearOfBirth' not in params
    sex = 'sex' not in params
    mail = 'mail' not in params
    phone = 'phone' not in params
    carringAgency = 'carringAgency' not in params
    goalOfApplication = 'goalOfApplication' not in params
    scheduleType = 'scheduleType' not in params
    transportIssue = 'transportIssue' not in params
    success = 'success' not in params
    dateBeginning = 'dateBeginning' not in params
    daysSelected = 'daysSelected' not in params
    daysInterval = 'daysInterval' not in params
    comment = 'comment' not in params
    streetHome =  'streetHome' not in params
    homeIntercommunity = 'homeIntercommunity' not in params
    homeDept = 'homeDept' not in params
    streetWork = 'streetWork' not in params
    workIntercommunity = 'workIntercommunity' not in params
    data = []
    if idCalendar:
        data.append('id')
    if dateRegister:
        data.append('Date d\'Inscription')
    if firstname:
        data.append(u'Prénom'.encode('latin-1'))
    if name:
        data.append('Nom')
    if yearOfBirth:
        data.append(u'Année de naissance'.encode('latin-1'))
    if sex:
        data.append('Sexe')
    if mail:
        data.append('Mail')
    if phone:
        data.append(u'Téléphone'.encode('latin-1'))
    if carringAgency:
        data.append('Structure d\'accompagnement')
    if goalOfApplication:
        data.append('But de la demande')
    if scheduleType:
        data.append('Type de Planning')
    if transportIssue:
        data.append(u'Problème de transport'.encode('latin-1'))
    if success:
        data.append('Validation')
    if comment:
        data.append('Commentaire de validation')
    if dateBeginning:
        data.append('Date de la demande')
    if daysSelected:
        data.append(u'Nombre de jours demandés'.encode('latin-1'))
    if daysInterval:
        data.append(u'Période de la demande'.encode('latin-1'))
    if streetHome:
        data.append('Adresse du Domicile')
    if homeIntercommunity:
        data.append(u'COMCOM (Domicile)'.encode('latin-1'))
    if homeDept:
        data.append(u'Département (Domicile)'.encode('latin-1'))
    if streetWork:
        data.append('Adresse du travail')
    if workIntercommunity:
        data.append(u'COMCOM (Travail)'.encode('latin-1'))
    return [data]


def generate_applicants_row(data, i, calendar, params, intercommunities, previous_calendar, index_of):
    idCalendar = 'idCalendar' not in params
    dateRegister = 'dateRegister' not in params
    firstname = 'firstname' not in params
    name = 'name' not in params
    yearOfBirth = 'yearOfBirth' not in params
    sex = 'sex' not in params
    mail = 'mail' not in params
    phone = 'phone' not in params
    carringAgency = 'carringAgency' not in params
    goalOfApplication = 'goalOfApplication' not in params
    scheduleType = 'scheduleType' not in params
    transportIssue = 'transportIssue' not in params
    success = 'success' not in params
    dateBeginning = 'dateBeginning' not in params
    daysSelected = 'daysSelected' not in params
    daysInterval = 'daysInterval' not in params
    comment = 'comment' not in params
    streetHome = 'streetHome' not in params
    homeIntercommunity = 'homeIntercommunity' not in params
    homeDept = 'homeDept' not in params
    streetWork = 'streetWork' not in params
    workIntercommunity = 'workIntercommunity' not in params
    if previous_calendar and previous_calendar[index_of['idApplicant']] == calendar[index_of['idApplicant']]:
        r = are_neighbours(calendar, previous_calendar, index_of)
        if daysInterval:
            n_interval = data[0].index(u'Période de la demande'.encode('latin-1'))
        if daysSelected:
            n_days = data[0].index(u'Nombre de jours demandés'.encode('latin-1'))
        if success:
            n_success = data[0].index('Validation')
        if r == 1:
            if daysInterval:
                data[i-1][n_interval] = get_full_intervals(data[i-1][n_interval]) + calendar[index_of['intervalDays']]
            if daysSelected:
                data[i-1][n_days] += calendar[index_of['selectedDays']]
            if success:
                data[i-1][n_success] = (int(data[i-1][n_success]) + calendar[index_of['success']])/2
            return data, 0
    '''index_of = {'idApplicant': 0, 'dateRegister': 1, 'firstname': 2, 'name': 3, 'yearOfBirth': 4, 'sex': 5, 'mail': 6,
                'phone': 7, 'carringAgency': 8, 'goalOfApplication': 9, 'scheduleType': 10, 'transportIssue': 11,
                'success': 12, 'comment': 13, 'dateBeginning': 14, 'selectedDays': 15, 'intervalDays': 16, 'streetHome': 17,
                'homeDept':18, 'streetWork': 19, 'firstWeek': 20, 'lastWeek': 21}'''
    if idCalendar:
        data[i].append(calendar[index_of['idApplicant']])
    if dateRegister:
        data[i].append(calendar[index_of['dateRegister']].strftime('%d/%m/%Y'))
    if firstname:
        data[i].append(calendar[index_of['firstname']])
    if name:
        data[i].append(calendar[index_of['name']])
    if yearOfBirth:
        data[i].append(calendar[index_of['yearOfBirth']])
    if sex:
        data[i].append(calendar[index_of['sex']])
    if mail:
        data[i].append(calendar[index_of['mail']])
    if phone:
        data[i].append(calendar[index_of['phone']])
    if carringAgency:
        data[i].append(calendar[index_of['carringAgency']])
    if goalOfApplication:
        data[i].append(calendar[index_of['goalOfApplication']])
    if scheduleType:
        data[i].append(calendar[index_of['scheduleType']])
    if transportIssue:
        data[i].append(calendar[index_of['transportIssue']])
    if success:
        data[i].append(calendar[index_of['success']])
    if comment:
        data[i].append(calendar[index_of['comment']])
    if dateBeginning:
        data[i].append(calendar[index_of['dateBeginning']])
    if daysSelected:
        data[i].append(calendar[index_of['selectedDays']])
    if daysInterval:
        data[i].append(calendar[index_of['intervalDays']])
    if streetHome:
        data[i].append(calendar[index_of['streetHome']].encode('latin-1'))
    if homeIntercommunity:
        address = calendar[index_of['streetHome']]
        data[i].append(get_intercommunity(intercommunities, address))
    if homeDept:
        data[i].append(calendar[index_of['homeDept']])
    if streetWork:
        data[i].append(calendar[index_of['streetWork']].encode('latin-1'))
    if workIntercommunity:
        address = calendar[index_of['streetWork']]
        data[i].append(get_intercommunity(intercommunities, address))
    return data, 1

'''
    Return 0 if false, 1 if calendar is after previous_calendar, -1 if calendar is before previous_calendar
'''
def are_neighbours(calendar, previous_calendar, index_of):
    if calendar[index_of['idApplicant']] == previous_calendar[index_of['idApplicant']]:
        if previous_calendar[index_of['lastWeek']]+1 == calendar[index_of['firstWeek']]:
            return 1
        if calendar[index_of['lastWeek']]+1 == previous_calendar[index_of['firstWeek']]:
            return -1
    return 0

'''
    From the current interval, returns a new interval counting every day (multiple of 14)
'''
def get_full_intervals(n):
    i = 0
    while n>=0:
        n-=14
        i+=1
    return i*14


def get_departement(zipCode):
    if zipCode[:2] == "35":
        return u'Ille-et-Vilaine'.encode('latin-1')
    elif zipCode[:2] == "29":
        return u'Finistère'.encode('latin-1')
    elif zipCode[:2] == "56":
        return u'Morbihan'.encode('latin-1')
    else:
        return ""


def get_intercommunities():
    query_intercommunities = Intercommunity.objects.select_related('town','intercommunity').values('town','intercommunity')
    intercommunities = []
    for intercom in query_intercommunities:
        intercommunities.append((intercom['town'], intercom['intercommunity']))
    return intercommunities


def get_intercommunity(intercommunities, street):
    street = street.replace(', France', '').replace(', Bretagne','')
    import unicodedata
    street = unicodedata.normalize("NFKD", street ).encode("ascii","ignore").strip()
    for intercom in intercommunities:
        comcom = unicodedata.normalize("NFKD", intercom[0]).encode("ascii","ignore")
        if comcom.lower().startswith(street.lower()[-(comcom.__len__())::]):
            return intercom[1]
    return ""


def sameIntercommunity(street, intercom, intercoms):
    intercom2 = get_intercommunity(intercoms, street)
    return intercom == intercom2


def get_data_user_register(user_register, start, end, format, total=False, weeks=False):
    earliest_date = User.objects.earliest('dateRegister').dateRegister
    latest_date = datetime.today()
    if start == "0":
        starting_date = earliest_date
    else:
        starting_date = start
    if end == "0":
        end_date = datetime.today()
    else:
        end_date = end
    all_delta = latest_date-earliest_date
    all_dates_raw = [(earliest_date+timedelta(days=x)).strftime(format) for x in range(all_delta.days + 1)]
    all_dates = []
    for d in all_dates_raw:
        if d not in all_dates:
            all_dates.append(d)
    delta = end_date-starting_date
    dates_raw = [(starting_date+timedelta(days=x)).strftime(format) for x in range(delta.days + 1)]
    dates = []
    for d in dates_raw:
        if d not in dates:
            dates.append(d)
    data = {'counter': [], 'date': []}
    if total:
        nb_total = 0
        print all_dates
        print dates
        for d in dates:
            for u in user_register:
                if u['dateR'] == d:
                    nb_total += u['nb']
            data['date'].append(d)
            data['counter'].append(nb_total)
    else:
        for d in dates:
            print d
            nb = 0
            for u in user_register:
                if u['dateR'] == d:
                    nb += u['nb']
            data['date'].append(d)
            data['counter'].append(nb)
    if weeks:
        new_data = {'counter': [], 'date': []}
        len = data['counter'].__len__()
        if not total:
            for i in range(0,len):
                if i%7 == 0:
                    new_data['date'].append(data['date'][i])
                    new_counter = 0
                new_counter += data['counter'][i]
                if i%7 == 6 or data['date'][i] == datetime.strftime(end_date, format):
                    new_data['counter'].append(new_counter)
        else:
            for i in range(0,len):
                if i%7 == 0:
                    new_data['date'].append(data['date'][i])
                if i%7 == 6 or data['date'][i] == datetime.strftime(end_date, format):
                    new_data['counter'].append(data['counter'][i])
        data = new_data
    return data