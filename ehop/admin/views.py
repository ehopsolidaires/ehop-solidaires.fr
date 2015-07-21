# -*- coding: utf-8 -*-

# @copyright (C) 2014-2015
# Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN'
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django.shortcuts import *
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User as django_user
from datetime import *
from ehopSolidaire_providers_register.forms import *
from ehopSolidaire_providers_register.models import SMS as SMS_model
from ehopSolidaire_providers_register.views import getCompaniesList
from forms import *
from forms import UserRegisterForm2
from ehopSolidaire_providers_register.forms import AddressRegisterForm, AddressRegisterFormWork, \
    PathArrivalRegisterForm, PathDepartureRegisterForm
from decorators import staff_member_required
import math
import sms as sms_api
from charts import *
import json
import csv

@staff_member_required
def generate_chart(request, id, dates, params):
    if params:
        params = params.split('_')
    dates = dates.split('_')
    if dates[0] != "0":
        start_date = datetime.strptime(dates[0], '%d%m%Y')
    else:
        start_date = "0"
    if dates[1] != "0":
        end_date = datetime.strptime(dates[1], '%d%m%Y') + timedelta(days=1, seconds=-1)
    else:
        end_date = "0"
    data = {}
    if id == "1":
        data['chart_data'] = ChartData.get_provider_date_register(params[0], params[1], params[2], start_date, end_date)
    elif id == "2":
        data['chart_data'] = ChartData.get_provider_total_registered(params[0], params[1], params[2], start_date, end_date)
    elif id == "3":
        data['chart_data'] = ChartData.get_counters_provider_applicant(params[0], params[1], start_date, end_date)
    elif id == "4":
        data['chart_data'] = ChartData.get_chart_unsubs(params[0], params[1], params[2], start_date, end_date)
    elif id == "5":
        data['chart_data'] = ChartData.get_chart_provider_origins(params[0], start_date, end_date)
    return HttpResponse(json.dumps(data), content_type='application/json')


@staff_member_required
def generate_csv(request, id, dates, params=None):
    response = HttpResponse(content_type='text/csv')
    if id == '4':
        if params:
            params = params.split('_')
        else:
            params = []
        dates = dates.split('_')
        data = ChartData.get_all_providers_info(dates[0], dates[1], params)
        filename = "export_stats_Offreurs"
    elif id == '5':
        if params:
            params = params.split('_')
        else:
            params = []
        dates = dates.split('_')
        data = ChartData.get_all_applicants_info(dates[0], dates[1], params)
        filename = "export_stats_Demandes"
    elif id == '6':
        dates = dates.split('_')
        data = ChartData.get_car_sharings(dates[0],dates[1])
        filename = "export_stats_MER"
    elif id == '7':
        dates = dates.split('_')
        data = ChartData.get_unsubs(dates[0],dates[1])
        filename = "export_stats_Desinscriptions"
    '''keys = data.keys()
    writer = csv.writer(response, delimiter=';')
    writer.writerow([key.encode('latin-1') for key in keys])
    for i in range(0, data[keys[0]].__len__()):
        row = []
        for key in keys:
            row.append(str(data[key][i]).encode('latin-1'))
        writer.writerow(row)'''
    writer = csv.writer(response, delimiter=';')
    writer.writerows(data)
    response['Content-Disposition'] = 'attachment; filename="'+filename+date_filename(dates)+'.csv"'
    return response


def date_filename(dates):
    if dates[0] == "0" and dates[1] == "0":
        return ""
    suffix = "_"
    if dates[0] != "0" and dates[1] != "0":
        date0 = datetime.strptime(dates[0], "%d%m%Y")
        date1 = datetime.strptime(dates[1], "%d%m%Y")
        return suffix+date0.strftime("%d-%m-%Y")+"_"+date1.strftime("%d-%m-%Y")
    elif dates[1] != "0":
        date1 = datetime.strptime(dates[1], "%d%m%Y")
        return suffix+date1.strftime("%d-%m-%Y")
    elif dates[0] != "0":
        date0 = datetime.strptime(dates[0], "%d%m%Y")
        return suffix+date0.strftime("%d-%m-%Y")


@staff_member_required
def stats(request):
    intercommunities = Intercommunity.objects.values_list('intercommunity', flat=True).order_by('intercommunity').distinct()
    return render(request, 'admin/stats.html',{'optionsCOMCOM':intercommunities})


@staff_member_required
def sms(request, provider_id, calendar_id):
    noStop = False
    current_calendar = Calendar.objects.get(idCalendar=calendar_id)
    beginning = current_calendar.get_beginning_date().strftime('%d/%m')
    interval_days = current_calendar.get_interval_days()
    sms_api.update()
    if request.method == "POST":
        message = request.POST.get('message')
        current_provider = Provider.objects.get(idProvider=provider_id)
        r = sms_api.send(receiver=current_provider.idUser.phone, tag=calendar_id, message=message, noStop=noStop)
        if r != 0:
            messages.error(request, "Envoi: " + str(r))
            return HttpResponseRedirect('/BO/')
    placeholder_sms = u"Ehop Solidaires\nNous cherchons un conducteur solidaire.\nTrajet : "+current_calendar.get_path()+\
                      u"\nA partir du "+str(beginning)+\
                      u"\nSur "+str(interval_days)+u"jrs" \
                      u"\nRépondez par SMS(non surtaxé) ou Appelez le 0299350130"
    provider = Provider.objects.get(idProvider=provider_id)
    list_sms = sms_api.get_sms_list(provider.idUser.phone)
    today = datetime.today()
    for s in list_sms:
        if s.date.date() < today.date():
            s.date = s.date.date()
        else:
            s.date = s.date.time()
    return render(request, 'admin/sms_chat.html', {'list_sms': list_sms, 'provider': provider,
                                                   'placeholder_sms': placeholder_sms, 'noStop':noStop})


def sms_new(request):
    import time
    timer = time.time()
    sms_api.update()
    query_new = SMS_model.objects.filter(read=False).values('sender').annotate(total=Count('sender'))
    list_new = list()
    for new in query_new:
        provider = Provider.objects.filter(idUser_id__phone=new['sender'])
        new['provider'] = provider[0]
        provider_sms = SMS_model.objects.filter(Q(read=False) & Q(sender=provider[0].idUser.phone))
        list_calendars_id = list()
        list_tag = list()
        for s in provider_sms:
            if s.tag not in list_tag:
                try:
                    calendar = Calendar.objects.get(idCalendar=s.tag)
                except ObjectDoesNotExist:
                    calendar = s.tag
                list_tag.append(s.tag)
                list_calendars_id.append(calendar)
        new['idCalendars'] = list_calendars_id
        list_new.append(new)
    print time.time() - timer
    return render(request, 'admin/sms_new.html', {'list_new': list_new})


'''
    Print all the providers
'''
@staff_member_required
def users(request):
    return render(request,'admin/utilisateurs.html', {})


'''
    Search and order providers and applicant
'''


@staff_member_required
def search_order(request):
    #on verifie si l'on souhaite recuperer offreur ou demandeur
    if ('user' in request.GET) and request.GET['user'].strip():
        query_user = request.GET['user']
        if query_user == "demandeur":
            user_info = Applicant.objects.all().order_by('-idUser__dateRegister')
        else:
            user_info = Provider.objects.all().order_by('-idUser__dateRegister')
        counter = user_info.count()
    else:
        raise Http404
    #inisitalisation du nb de resultat par page
    query_nbresult = 20

    #Si une requete search est effectue
    if ('search' in request.GET) and request.GET['search'].strip():
        query_search = request.GET['search']
        user_info = user_info.filter(Q(idUser__name__icontains=query_search) |
                                     Q(idUser__firstname__icontains=query_search) |
                                     Q(idUser__idWorkAddress__city__icontains=query_search) |
                                     Q(idUser__idHomeAddress__city__icontains=query_search) |
                                     Q(idUser__idWorkAddress__street__icontains=query_search) |
                                     Q(idUser__idHomeAddress__street__icontains=query_search))

    if ('order' in request.GET) and request.GET['order'].strip():
        query_order = request.GET['order']
        if query_order != 'dateRegister':
            if query_order[0] == '-':
                user_info = user_info.order_by('-idUser__' + query_order[1:])
            else:
                user_info = user_info.order_by('idUser__' + query_order)

    if ('nbResult' in request.GET) and request.GET['nbResult'].strip():
        query_nbresult = request.GET['nbResult']

    if query_user == "demandeur":
        dict_app = []
        for user in user_info:
            calendars = Calendar.objects.filter(idApplicant=user.idApplicant)
            if calendars:
                success = 0.0
                for calendar in calendars:
                    success += calculate_success(calendar)
                success /= calendars.__len__()
            else:
                success = None
            dict_app.append({'cityW': user.idUser.idWorkAddress.city,
                             'cityH': user.idUser.idHomeAddress.city,
                             'streetH': user.idUser.idHomeAddress.street,
                             'streetW': user.idUser.idWorkAddress.street,
                             'firstname': user.idUser.firstname,
                             'name': user.idUser.name,
                             'idApplicant': user.idApplicant,
                             'success': success})
        user_info = dict_app
    #affiche 2 user par page
    paginator = Paginator(user_info, query_nbresult)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    range3 = [1]
    if paginator.num_pages > 1:
        range3.append(2)
    if users.number != 1 and users.number != 2 and users.number != paginator.num_pages - 1 and users.number \
            != paginator.num_pages:
        range3.append(users.number)
    if paginator.num_pages - 1 > 2:
        range3.append(paginator.num_pages - 1)
    if paginator.num_pages > 2:
        range3.append(paginator.num_pages)
    return render(request,
                  'admin/resultats.html', {'user_info': users, 'range2': range3, 'counter': counter})


@staff_member_required
def bo(request):
    return render(request,
                  'admin/bo.html', {})


@staff_member_required
def add_applicant(request):
    msg = ''
    if request.method == 'POST':
        user_form = UserRegisterForm2(request.POST)
        applicant_form = ApplicantRegisterForm(request.POST)
        calendar_form = CalendarForm(request.POST)
        address_home_form = AddressRegisterForm(request.POST, prefix="home")
        address_work_form = AddressRegisterFormWork(request.POST, prefix="work")
        if not user_form.is_valid():
            u = user_form.instance
            if u.mail != "":
                msg = "Cette adresse mail est déjà utilisée."
            else:
                msg = "Il existe une erreur dans les informations que vous avez entrees, veuillez recommencer."
            msg = user_form.errors
        elif not applicant_form.is_valid():
            a = applicant_form.instance
            if a.identNum == "" or a.identNum == None:
                msg = "Il existe une erreur dans les informations que vous avez entrées, veuillez recommencer."
            else:
                msg = "Cet Identifiant existe déjà"
            msg = applicant_form.errors
        elif not address_home_form.is_valid():
            msg = "Il existe une erreur dans l'adresse du point de départ"
        elif not address_work_form.is_valid():
            msg = "Il existe une erreur dans l'adresse du point d'arrivée"
        elif not calendar_form.is_valid():
            msg = "Il existe une erreur dans le calendrier"
        else:
            listGo = ""
            listBack = ""
            for i in range(0, 14):
                if request.POST.get("go-" + str(i)):
                    listGo += "R"
                else:
                    listGo += "G"
                if request.POST.get("back-" + str(i)):
                    listBack += "R"
                else:
                    listBack += "G"
                if i < 13:
                    listGo += ","
                    listBack += ","
            calendar_form.instance.go = listGo
            calendar_form.instance.back = listBack
            if (calendar_form.cleaned_data['scheduleBeginningGo'] > calendar_form.cleaned_data[
                'scheduleBeginningBack']):
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo + timedelta(days=1)
            else:
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo

            address_home = address_home_form.save(commit=False)
            address_home.point = address_home_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad = Address.objects.filter(point=address_home.point)
            if queryad:
                #On recupere l'adresse deja stocke
                address_home = queryad[0]
            else:
                #sinon on sauvegarde la nouvelle
                address_home.zipCode = address_home_form.cleaned_data['zipCode']
                address_home.city = address_home_form.cleaned_data['city']
                address_home.save()

            address_work = address_work_form.save(commit=False)
            address_work.point = address_work_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad = Address.objects.filter(point=address_work.point)
            if queryad:
                #Au cas ou plusieurs adresse identique se trouveraient deja dans la bdd
                address_work = queryad[0]
            else:
                #sauvegarde de la nouvelle adresse
                address_work.zipCode = address_work_form.cleaned_data['zipCode']
                address_work.city = address_work_form.cleaned_data['city']
                address_work.save()

            user_form.instance.idHomeAddress_id = address_home.pk
            user_form.instance.idWorkAddress_id = address_work.pk
            user = user_form.save()

            applicant_form.instance.idUser_id = user.pk
            applicant = applicant_form.save()

            calendar_form.instance.idApplicant_id = applicant.pk
            calendar_form.instance.streetHome = address_home_form.instance.street
            calendar_form.instance.streetWork = address_work_form.instance.street
            current_calendar = calendar_form.save()
            LinkCalendar(idCalendar=current_calendar, idApplicant=applicant).save()
            return HttpResponseRedirect("/BO/utilisateurs/d/" + str(applicant.pk) + "/")

    user_form = UserRegisterForm2()
    applicant_form = ApplicantRegisterForm()
    calendar_form = CalendarForm()
    address_home_form = AddressRegisterForm(prefix="home")
    address_work_form = AddressRegisterFormWork(prefix="work")
    messages.error(request, msg)
    return render(request, 'admin/add_applicant.html',
                  {'user_form': user_form, 'applicant_form': applicant_form, 'address_home_form': address_home_form,
                   'address_work_form': address_work_form, 'calendar_form': calendar_form})


'''
    Modify informations about a provider
'''


@staff_member_required
def provider(request, provider_id):
    msg = ''
    #on recupere l offreur correspondant
    try:
        current_provider = Provider.objects.get(idProvider=provider_id)
    except ObjectDoesNotExist:
        messages.error(request, "Cet offreur n'exsite pas.")
        return HttpResponseRedirect("/BO/")
    #on recupere l'utilisateur connecte
    current_user = current_provider.idUser

    #on sauvegarde le mail pour modifier la connexion dans django
    current_user_mail = current_user.mail

    path_departure_register_form_set = formset_factory(PathDepartureRegisterForm)
    path_arrival_register_form_set = formset_factory(PathArrivalRegisterForm)
    if request.method == 'POST':
        if request.POST.get('supprimer'):
            try:
                django_u = django_user.objects.get(Q(username=current_user.mail) | Q(email=current_user.mail))
            except ObjectDoesNotExist:
                django_u = None
            if django_u:
                django_u.delete()
            intercoms = get_intercommunities()
            Deletion.objects.create(dateDelete=datetime.now(),dateRegister=current_user.dateRegister,
                                    type="provider", reason=request.POST.get('supprimer'),
                                    homeIntercommunity=get_intercommunity(intercoms,current_user.idHomeAddress.street),
                                    homeZipCode=current_user.zipCode,
                                    workIntercommunity=get_intercommunity(intercoms,current_user.idWorkAddress.street))
            current_user.delete()
            return HttpResponseRedirect('/BO/utilisateurs/?u=offreur')
        startingWeek = request.POST.get("startingWeek", "")
        user_form = TestUserRegisterForm(request.POST, instance=current_user)
        provider_form = ProviderForm2(request.POST, instance=current_provider)
        address_home_form = AddressRegisterForm(request.POST, prefix="home")
        address_work_form = AddressRegisterFormWork(request.POST, prefix="work")
        path_departure_register_formset = path_departure_register_form_set(request.POST, prefix="departure")
        path_arrival_register_formset = path_arrival_register_form_set(request.POST, prefix="arrival")
        if not user_form.is_valid():
            print user_form
        elif not address_home_form.is_valid():
            print address_home_form
            print 'error address'
        elif not address_work_form.is_valid():
            print address_work_form
            print 'error address'
        elif not path_departure_register_formset.is_valid():
            print 'error horaire depart'
        elif not path_arrival_register_formset.is_valid():
            print 'error horaire arrivee'
        elif not provider_form.is_valid():
            print 'error company'
            print provider_form.errors
        else:
            Provider.objects.filter(idProvider=current_provider.idProvider).update(
                company=provider_form.cleaned_data['company'], howKnowledge=provider_form.cleaned_data['howKnowledge'])
            address_home = address_home_form.save(commit=False)
            address_home.point = address_home_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad = Address.objects.filter(point=address_home.point)
            if queryad:
                #On recupere l'adresse deja stocke
                address_home = queryad[0]
            else:
                #sinon on sauvegarde la nouvelle
                address_home.zipCode = address_home_form.cleaned_data['zipCode']
                address_home.city = address_home_form.cleaned_data['city']
                address_home.save()

            address_work = address_work_form.save(commit=False)
            address_work.point = address_work_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad = Address.objects.filter(point=address_work.point)
            if queryad:
                #On recupere l'adresse deja stocke
                address_work = queryad[0]
            else:
                #sinon on sauvegarde la nouvelle
                address_work.zipCode = address_work_form.cleaned_data['zipCode']
                address_work.city = address_work_form.cleaned_data['city']
                address_work.save()

            #Sauvegarde des données personnelles
            user_form.instance.idHomeAddress_id = address_home.pk
            user_form.instance.idWorkAddress_id = address_work.pk
            user_form.save()

            #modification de ladresse dans django
            django_user.objects.filter(email=current_user_mail).update(email=current_user.mail)

            #on supprimme les anciennes horaires
            #TODO: update plutot que supprimer et recreer
            paths = Path.objects.filter(idProvider=current_provider)
            for path in paths:
                path.delete()

            for departure_form in path_departure_register_formset:
                departure_form.instance.idProvider_id = current_provider.pk
                departure_form.instance.departure_id = address_home.pk
                departure_form.instance.arrival_id = address_work.pk
                departure_form.instance.startingWeek = startingWeek
                if departure_form.is_valid() and departure_form.has_changed():
                    departure_form.save()

            for arrival_form in path_arrival_register_formset:
                arrival_form.instance.idProvider_id = current_provider.pk
                arrival_form.instance.departure_id = address_work.pk
                arrival_form.instance.arrival_id = address_home.pk
                arrival_form.instance.startingWeek = startingWeek
                if arrival_form.is_valid() and arrival_form.has_changed():
                    arrival_form.save()

    user_form = TestUserRegisterForm(
        initial={'name': current_user.name, 'firstname': current_user.firstname, 'city': current_user.city,
                 'zipCode': current_user.zipCode, 'mail': current_user.mail, 'sex': current_user.sex,
                 'phone': current_user.phone})
    provider_form = ProviderForm2(initial={'company': current_provider.company,'howKnowledge':current_provider.howKnowledge})
    address_home_form = AddressRegisterForm(initial={'street': current_user.idHomeAddress.street}, prefix="home")
    address_work_form = AddressRegisterFormWork(initial={'street': current_user.idWorkAddress.street}, prefix="work")

    #on recupere les trajets
    paths = Path.objects.filter(idProvider=current_provider).order_by('idPath')
    path_departure_register_formset = path_departure_register_form_set(prefix="departure")
    path_arrival_register_formset = path_arrival_register_form_set(prefix="arrival")
    return render(request, 'admin/provider_update.html', {
        'user_form': user_form,
        'address_home_form': address_home_form,
        'address_work_form': address_work_form,
        'provider_form': provider_form,
        'path_departure_register_formset': path_departure_register_formset,
        'path_arrival_register_formset': path_arrival_register_formset,
        'companiesList': getCompaniesList(),
        'paths': paths,
    })


'''
    Modify informations about an applicant
'''
@staff_member_required
def applicant(request, applicant_id):
    msg = ''
    try:
        current_applicant = Applicant.objects.get(idApplicant=applicant_id)
    except ObjectDoesNotExist:
        messages.error(request, "Ce demandeur n'existe pas.")
        return HttpResponseRedirect("/BO/")
    current_user = current_applicant.idUser
    current_calendars = LinkCalendar.objects.filter(idApplicant=current_applicant)

    if request.method == 'POST':
        if request.POST.get('supprimer'):
            current_user.delete()
            return HttpResponseRedirect('/BO/utilisateurs/?u=demandeur')
        elif request.POST.get('delete'):
            try:
                current_calendar = Calendar.objects.get(idCalendar=request.POST.get('delete'))
            except ObjectDoesNotExist:
                messages.error(request, "Impossible d'archiver ce calendrier, celui-ci n'existe plus.")
                return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_applicant.idApplicant) + '/')
            current_calendar.delete()
            messages.error(request, 'Calendrier supprimé.')
            return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_applicant.idApplicant) + '/')
        # save modifications
        user_form = UserRegisterForm2(request.POST, instance=current_user)
        applicant_form = ApplicantRegisterForm(request.POST, instance=current_applicant)
        if not user_form.is_valid():
            u = user_form.instance
            if u.mail == "":
                msg = "Vous  n'avez pas entre d'adresse mail."
            elif u.mail != "":
                msg = "Cette adresse mail est déjà utilisée."
            else:
                msg = "Il existe une erreur dans les informations que vous avez entrees, veuillez recommencer."
                msg = user_form.errors
        elif not applicant_form.is_valid():
            msg = "Il existe une erreur dans les informations que vous avez entrees, veuillez recommencer."
            msg = applicant_form.errors
        else:
            user_form.instance.idHomeAddress_id = current_user.idHomeAddress
            user_form.instance.idWorkAddress_id = current_user.idWorkAddress
            user = user_form.save()

            applicant_form.instance.idUser_id = user.pk
            applicant_form.save()

            comments_name_list = [key for key in request.POST if key.startswith("comments-")]
            for comments_name in comments_name_list:
                idCalendar = comments_name.replace("comments-", "")
                comments = request.POST.get(comments_name)
                Calendar.objects.filter(idCalendar=int(idCalendar)).update(comments=comments)
            msg = "Le demandeur a été modifié."
            print request.POST
            if request.POST.get('archiveCalendar'):
                try:
                    current_calendar = Calendar.objects.get(idCalendar=request.POST.get('archiveCalendar'))
                except ObjectDoesNotExist:
                    messages.error(request, "Impossible d'archiver ce calendrier, celui-ci n'existe plus.")
                    return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_applicant.idApplicant) + '/')
                pourcentage = calculate_success(current_calendar)
                idApplicant = current_calendar.idApplicant
                dateBeginning = current_calendar.dateBeginningGo
                scheduleBeginningGo = current_calendar.scheduleBeginningGo
                scheduleBeginningBack = current_calendar.scheduleBeginningBack
                go = current_calendar.go
                back = current_calendar.back
                possibleMeetingSpot = current_calendar.possibleMeetingSpot
                streetHome = current_calendar.streetHome
                streetWork = current_calendar.streetWork
                transportIssue = current_calendar.transportIssue
                print request.POST.get('comment')
                comment = request.POST.get('comment')
                comments = current_calendar.comments
                histocal = HistoricCalendar.objects.create(pourcentage=pourcentage, idApplicant=idApplicant,
                                            dateBeginning=dateBeginning, scheduleBeginningGo=scheduleBeginningGo,
                                            scheduleBeginningBack=scheduleBeginningBack, go=go, back=back,
                                            streetHome=streetHome, streetWork=streetWork,
                                            possibleMeetingSpot=possibleMeetingSpot,
                                            comment=comment, transportIssue=transportIssue,
                                            comments=comments)
                #archive validated researchs of this calendar
                starting_date = current_calendar.dateBeginningGo
                researchs = Research.objects.filter(idCalendar=current_calendar.pk).order_by('idResearch')
                if researchs:
                    i = 0
                    idPath = researchs[0].idPath.idPath
                    for r in researchs:
                        if r.idPath.idPath != idPath:
                            i = 0
                            idPath = r.idPath.idPath
                        date = starting_date + timedelta(days=i)
                        r.archive(date, histocal)
                        i += 1
                current_calendar.delete()
                messages.error(request, 'Calendrier archivé.')
                return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_applicant.idApplicant) + '/')
    dict_CalForm = []
    form_set = formset_factory(CalendarFormDisplay, extra=0)
    for set in current_calendars:
        current_calendar = set.idCalendar
        dict_CalForm.append({
            'idApplicant': current_calendar.idApplicant, 'dateBeginningGo': current_calendar.dateBeginningGo,
            'scheduleBeginningGo': current_calendar.scheduleBeginningGo,
            'scheduleBeginningBack': current_calendar.scheduleBeginningBack,
            'dateBeginningBack': current_calendar.dateBeginningBack, 'go': current_calendar.go,
            'back': current_calendar.back, 'streetHome': current_calendar.streetHome,
            'streetWork': current_calendar.streetWork,
            'possibleMeetingSpot': current_calendar.possibleMeetingSpot,
            'address_home': current_calendar.streetHome,
            'address_work': current_calendar.streetWork,
            'listGo': current_calendar.go.split(","),
            'listBack': current_calendar.back.split(","),
            'listDaysName': create_daysName_list(current_calendar.dateBeginningGo.weekday()),
            'listDaysNum': create_daysNum_list(current_calendar.dateBeginningGo, 14),
            'idCalendar': current_calendar.idCalendar,
            'transportIssue': current_calendar.transportIssue,
            'success': calculate_success(current_calendar),
            'comments': current_calendar.comments})
    calendar_formset = form_set(initial=dict_CalForm)

    user_form = UserRegisterForm2(initial={'name': current_user.name, 'firstname': current_user.firstname,
                                           'city': current_user.city, 'zipCode': current_user.zipCode,
                                           'mail': current_user.mail, 'sex': current_user.sex,
                                           'phone': current_user.phone})
    applicant_form = ApplicantRegisterForm(initial={'carringAgency': current_applicant.carringAgency,
                                                    'accompName': current_applicant.accompName,
                                                    'accompFirstname': current_applicant.accompFirstname,
                                                    'accompPhone': current_applicant.accompPhone,
                                                    'accompMail': current_applicant.accompMail,
                                                    'goalOfApplication': current_applicant.goalOfApplication,
                                                    'identNum': current_applicant.identNum,
                                                    'scheduleType': current_applicant.scheduleType,
                                                    'yearOfBirth': current_applicant.yearOfBirth})
    options_0 = u'<option selected hidden value=""></option><option value="Abandon du demandeur">Abandon du demandeur</option><option value="Abandon de la structure accompagnante">Abandon de la structure accompagnante</option><option value="Pas de solution trouvée">Pas de solution trouvée</option><option value="Le demandeur a trouvé une autre solution">Le demandeur a trouvé une autre solution</option><option value="Hors cadre EHOP-solidaires">Hors cadre EHOP-solidaires</option>'.encode("utf-8")
    options = u'<option selected hidden value=""></option><option value="Deuxième solution trouvée par ses propres moyens">Deuxième solution trouvée par ses propres moyens</option><option value="Trajet complété par transports en commun">Trajet complété par transports en commun</option><option value="Pas de retour du demandeur">Pas de retour du demandeur</option>'
    messages.error(request, msg)
    return render(request, 'admin/applicant_update.html',
                  {'user_form': user_form, 'applicant_form': applicant_form,
                   'calendar_formset': calendar_formset, 'applicant_id': current_applicant.idApplicant,
                   'options_0':options_0, 'options':options})


'''
    Add a calendar to an applicant
'''
@staff_member_required
def add_calendar(request, applicant_id):
    msg = ''
    try:
        current_applicant = Applicant.objects.get(idApplicant=applicant_id)
    except ObjectDoesNotExist:
        current_applicant = None
    if request.method == 'POST':
        calendar_form = CalendarForm(request.POST)
        if not calendar_form.is_valid():
            msg = "Il existe une erreur dans le calendrier"
        else:
            listGo = ""
            listBack = ""
            for i in range(0, 14):
                if request.POST.get("go-" + str(i)):
                    listGo += "R"
                else:
                    listGo += "G"
                if request.POST.get("back-" + str(i)):
                    listBack += "R"
                else:
                    listBack += "G"
                if i < 13:
                    listGo += ","
                    listBack += ","
            calendar_form.instance.go = listGo
            calendar_form.instance.back = listBack
            if (calendar_form.cleaned_data['scheduleBeginningGo'] > calendar_form.cleaned_data[
                'scheduleBeginningBack']):
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo + timedelta(days=1)
            else:
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo

            calendar_form.instance.idApplicant_id = current_applicant.idApplicant
            calendar_form.instance.streetHome = request.POST.get("streetHome")
            calendar_form.instance.streetWork = request.POST.get("streetWork")
            current_calendar = calendar_form.save()
            LinkCalendar(idCalendar=current_calendar, idApplicant=current_applicant).save()
            msg = "Nouveau calendrier ajouté."
            messages.error(request, msg)
            return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_applicant.idApplicant) + '/')

    calendar_form = CalendarForm()

    messages.error(request, msg)
    return render(request, 'admin/add_calendar.html',
                  {'calendar_form': calendar_form})


def modify_calendar(request, calendar_id):
    msg = ''
    try:
        current_calendar = Calendar.objects.get(idCalendar=calendar_id)
    except ObjectDoesNotExist:
        msg = "Ce calendrier n'éxiste pas.".encode('utf-8')
        messages.error(request, msg)
        return HttpResponseRedirect('/BO/')
    if request.method == "POST":
        calendar_form = CalendarModifyForm(request.POST, instance=current_calendar)
        if not calendar_form.is_valid():
            msg = "Il existe une erreur dans le calendrier"
        else:
            listGo = ""
            listBack = ""
            for i in range(0, 14):
                if request.POST.get("go-" + str(i)):
                    listGo += "R"
                else:
                    listGo += "G"
                if request.POST.get("back-" + str(i)):
                    listBack += "R"
                else:
                    listBack += "G"
                if i < 13:
                    listGo += ","
                    listBack += ","
            calendar_form.instance.go = listGo
            calendar_form.instance.back = listBack
            if (calendar_form.cleaned_data['scheduleBeginningGo'] > calendar_form.cleaned_data[
                'scheduleBeginningBack']):
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo + timedelta(days=1)
            else:
                calendar_form.instance.dateBeginningBack = calendar_form.instance.dateBeginningGo
            calendar_form.save()
            msg = "Calendrier modifié."
            messages.error(request, msg)
            return HttpResponseRedirect('/BO/utilisateurs/d/' + str(current_calendar.idApplicant.idApplicant) + '/')
    calendar_dict = {
        'dateBeginningGo': current_calendar.dateBeginningGo.strftime('%d/%m/%Y'),
        'scheduleBeginningGo': current_calendar.scheduleBeginningGo,
        'scheduleBeginningBack': current_calendar.scheduleBeginningBack,
        'streetHome': current_calendar.streetHome,
        'streetWork': current_calendar.streetWork,
        'possibleMeetingSpot': current_calendar.possibleMeetingSpot,
        'transportIssue': current_calendar.transportIssue,
        'comments': current_calendar.comments
    }
    calendar_form = CalendarModifyForm(initial=calendar_dict)
    list_go = current_calendar.go.split(',')
    list_back = current_calendar.back.split(',')
    return render(request, 'admin/modify_calendar.html', {
        'calendar_form': calendar_form,
        'go': list_go,
        'back': list_back
    })


def formatDate(date):
    return date.strftime('%d/%m/%Y')


def reverseFormatDate(p_date):
    return date(int(p_date[6:]), int(p_date[3:-5]), int(p_date[:-8]))


@staff_member_required
def research(request, calendar_id):
    form_set = formset_factory(ResearchFormDisplay, extra=0)
    previousIsGo = None
    previousDeparture = None
    previousArrival = None
    if calendar_id != '0':
        try:
            current_calendar = Calendar.objects.get(idCalendar=calendar_id)
        except ObjectDoesNotExist:
            messages.error(request, "Impossible de faire une recherche pour ce calendrier, celui-ci n'existe plus.")
            return HttpResponseRedirect("/BO/")
        current_applicant = current_calendar.idApplicant
        listGo = current_calendar.go.split(",")
        listBack = current_calendar.back.split(",")
        homeWork = current_calendar.streetHome + "|" + current_calendar.streetWork
    else:
        current_calendar = None
        current_applicant = None
    if request.method == 'POST':
        research_form = ResearchForm(request.POST)
        if not research_form.is_valid():
            messages.error(request, research_form.errors)
            return render(request, 'admin/recherche.html',
                          {'applicant': current_applicant, 'research_form': research_form})
        previousDeparture = research_form.cleaned_data['departure']
        previousArrival = research_form.cleaned_data['arrival']
        if request.POST.get("research"):
            point_departure_demandeur = research_form.cleaned_data['departure_latlng']
            point_arrival_demandeur = research_form.cleaned_data['arrival_latlng']
            horaireMin = research_form.cleaned_data['timeMin'].split(':')
            horaireMin[0] = int(horaireMin[0])
            horaireMin[1] = int(horaireMin[1])
            horaireMax = research_form.cleaned_data['timeMax'].split(':')
            horaireMax[0] = int(horaireMax[0])
            horaireMax[1] = int(horaireMax[1])
            calendar = research_form.cleaned_data['date'].split(' ')
            beginningDate = calendar[0]
            if calendar[1] == 'Mon' or calendar[1] == '0':
                day = 'monday'
                starting_day = 0
            elif calendar[1] == 'Tue' or calendar[1] == '1':
                day = 'tuesday'
                starting_day = 1
            elif calendar[1] == 'Wed' or calendar[1] == '2':
                day = 'wednesday'
                starting_day = 2
            elif calendar[1] == 'Thu' or calendar[1] == '3':
                day = 'thursday'
                starting_day = 3
            elif calendar[1] == 'Fri' or calendar[1] == '4':
                day = 'friday'
                starting_day = 4
            elif calendar[1] == 'Sat' or calendar[1] == '5':
                day = 'saturday'
                starting_day = 5
            elif calendar[1] == 'Sun' or calendar[1] == '6':
                day = 'sunday'
                starting_day = 6
            coordTabH = point_departure_demandeur.replace('(', '').replace(')', '').split(',')
            coordTabW = point_arrival_demandeur.replace('(', '').replace(')', '').split(',')
            point_departure_demandeur = (float(coordTabH[0]), float(coordTabH[1]))
            point_arrival_demandeur = (float(coordTabW[0]), float(coordTabW[1]))
            if request.POST.get("isGo") == "true":
                isGo = True
            else:
                isGo = False
            previousIsGo = isGo

            # check already registered research for the applicant
            if current_applicant:
                #current_date = date(int(beginningDate[6:]), int(beginningDate[3:-5]), int(beginningDate[:-8]))
                applicant_researchs = Research.objects.filter(idCalendar=calendar_id).filter(Q(isGo=isGo))
                paths_already_saved = list()
                for set in applicant_researchs:
                    if set.idPath.idPath not in paths_already_saved:
                        paths_already_saved.append(set.idPath.idProvider)
                entry_list = list(Path.objects.filter(day__startswith=day).exclude(idProvider__in=paths_already_saved).select_related())
            else:
                entry_list = list(Path.objects.filter(day__startswith=day).select_related())
            liste = routeInEllipseFilter(point_departure_demandeur, point_arrival_demandeur, entry_list, 0.1)
            liste = fullRouteFilter(point_departure_demandeur, point_arrival_demandeur, liste, 0.1)
            liste = scheduleFilterIntervalle(horaireMin[0], horaireMin[1], horaireMax[0], horaireMax[1], liste)
            MAX = 50
            if liste.__len__() > MAX:
                maxsize = MAX
            else:
                maxsize = liste.__len__()
            formset_list = list()
            days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            dict_days_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                                 'sunday': 6}
            days = list()
            # 1 loop for each result
            for j in range(0, maxsize):
                dict_Rform = []
                path = liste[j]
                paths_of_provider = Path.objects.filter(idProvider=path.idProvider).filter(schedule=path.schedule).select_related('day')
                provider_days = list()

                # fills up the list of days possible for this provider
                for i in range(0, paths_of_provider.__len__()):
                    provider_days.append(paths_of_provider[i].day)

                mydate = date(int(beginningDate[6:]), int(beginningDate[3:-5]), int(beginningDate[:-8]))

                # 14 loops, to find the future days this provider is available
                for i in range(dict_days_of_week[day], dict_days_of_week[day] + 14):
                    if any(days_of_week[i % 7] in s for s in provider_days):
                        available = True
                    else:
                        available = False
                    dict_Rform.append({
                        'providerName': path.idProvider.idUser.firstname + " " + path.idProvider.idUser.name,
                        'providerDeparture': path.departure.street,
                        'providerArrival': path.arrival.street,
                        'providerId': path.idProvider.idProvider,
                        'idCalendar': calendar_id,
                        'idPath': path.idPath,
                        'detour': 0,
                        'detourkm': 0,
                        'streetDeparture': research_form.cleaned_data['departure'],
                        'streetArrival': research_form.cleaned_data['arrival'],
                        'validated': False,
                        'available': available,
                        'isGo': isGo}
                    )
                    if j == 0:
                        days.append(mydate.day)
                    mydate = addDay(mydate, 1)

                formset = form_set(initial=dict_Rform, prefix=j + 1)
                formset_list.append(formset)
            if current_applicant:
                research_form = ResearchForm(initial={'departure': current_calendar.streetHome,
                                                      'arrival': current_calendar.streetWork,
                                                      'previousDeparture': previousDeparture,
                                                      'previousArrival': previousArrival,
                                                      'timeGo': current_calendar.scheduleBeginningGo,
                                                      'timeBack': current_calendar.scheduleBeginningBack,
                                                      'dateGo': formatDate(current_calendar.dateBeginningGo),
                                                      'dateBack': formatDate(current_calendar.dateBeginningBack)})
                return render(request, 'admin/recherche.html',
                              {'applicant': current_applicant, 'formset_list': formset_list,
                               'research_form': research_form, 'days': days,
                               'days_list': create_daysName_list(starting_day),
                               'size_list_formset': maxsize,
                               'listGo': listGo, 'listBack': listBack,
                               'listDaysName': create_daysName_list(current_calendar.dateBeginningGo.weekday()),
                               'weekday': current_calendar.dateBeginningGo.weekday(),
                               'listDaysNum': create_daysNum_list(current_calendar.dateBeginningGo, 14),
                               'homeWork': homeWork, 'previousIsGo': previousIsGo})
            else:
                research_form = ResearchForm(initial={'departure': request.POST.get("departure"),
                                                      'arrival': request.POST.get("arrival"),
                                                      'previousDeparture': previousDeparture,
                                                      'previousArrival': previousArrival,
                                                      'timeMin': request.POST.get("timeMin"),
                                                      'timeMax': request.POST.get("timeMax"),
                                                      'date': request.POST.get("date")})
                return render(request, 'admin/recherche.html',
                              {'applicant': current_applicant, 'formset_list': formset_list,
                               'research_form': research_form, 'days': days,
                               'days_list': create_daysName_list(starting_day),
                               'size_list_formset': maxsize})
        else:
            size_list_formset = request.POST.get("size_list_formset")
            for i in range(1, int(size_list_formset) + 1):
                detour = 0
                detourkm = 0
                selected = False
                formset = form_set(request.POST, prefix=i)
                if formset.is_valid():
                    for counter, form in enumerate(formset):
                        if form.is_valid():
                            if (counter == 0):
                                detour = form.cleaned_data['detour']
                                detourkm = form.cleaned_data['detourkm']
                                selected = form.cleaned_data['selected']
                            else:
                                form.instance.detour = detour
                                form.instance.detourkm = detourkm
                                form.cleaned_data['selected'] = selected
                        if form.cleaned_data['selected']:
                            form.save()
                print formset.errors
            if request.POST.get("continue"):
                research_form = ResearchForm(initial={'departure': previousDeparture,
                                                      'arrival': previousArrival,
                                                      'previousDeparture': previousDeparture,
                                                      'previousArrival': previousArrival,
                                                      'timeGo': current_calendar.scheduleBeginningGo,
                                                      'timeBack': current_calendar.scheduleBeginningBack,
                                                      'dateGo': formatDate(current_calendar.dateBeginningGo),
                                                      'dateBack': formatDate(current_calendar.dateBeginningBack)})
                return render(request, 'admin/recherche.html', {'applicant': current_applicant,
                                                                'research_form': research_form,
                                                                'listGo': listGo, 'listBack': listBack,
                                                                'listDaysName': create_daysName_list(
                                                                    current_calendar.dateBeginningGo.weekday()),
                                                                'weekday': current_calendar.dateBeginningGo.weekday(),
                                                                'listDaysNum': create_daysNum_list(
                                                                    current_calendar.dateBeginningGo, 14),
                                                                'homeWork': homeWork, 'previousIsGo': previousIsGo})
            if request.POST.get("finish"):
                return redirect(applicant_search, calendar_id=current_calendar.idCalendar)
    if (current_applicant != None):
        research_form = ResearchForm(initial={'departure': current_calendar.streetHome,
                                              'arrival': current_calendar.streetWork,
                                              'previousDeparture': previousDeparture,
                                              'previousArrival': previousArrival,
                                              'timeGo': current_calendar.scheduleBeginningGo,
                                              'timeBack': current_calendar.scheduleBeginningBack,
                                              'dateGo': formatDate(current_calendar.dateBeginningGo),
                                              'dateBack': formatDate(current_calendar.dateBeginningBack)})
        return render(request, 'admin/recherche.html', {'applicant': current_applicant, 'research_form': research_form,
                                                        'listGo': listGo, 'listBack': listBack,
                                                        'listDaysName': create_daysName_list(
                                                            current_calendar.dateBeginningGo.weekday()),
                                                        'weekday': current_calendar.dateBeginningGo.weekday(),
                                                        'listDaysNum': create_daysNum_list(
                                                            current_calendar.dateBeginningGo, 14),
                                                        'homeWork': homeWork, 'previousIsGo': previousIsGo})
    else:
        research_form = ResearchForm()
        return render(request, 'admin/recherche.html', {'applicant': current_applicant, 'research_form': research_form})


def create_daysName_list(starting_day):
    init_days_list = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
    days_list = list()
    for i in range(starting_day, starting_day + 14):
        days_list.append(init_days_list[i % 7])
    return days_list


def create_daysNum_list(starting_date, listSize):
    list_days_num = list()
    for i in range(0, listSize):
        list_days_num.append(addDay(starting_date, i).day)
    return list_days_num


def getEarliestDay(paths_of_provider):
    order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day_list = []
    for i in range(0, paths_of_provider.__len__()):
        day_list.append(paths_of_provider[i].day)
    earliest_day = sorted(day_list, key=order.index)[0]
    for i in range(0, paths_of_provider.__len__()):
        if paths_of_provider[i].day == earliest_day:
            return paths_of_provider[i]
        else:
            return None


def addDay(date_given, to_add):
    return date_given + timedelta(days=to_add)


# First filter

def routeInEllipseFilter(point_home_demandeur, point_work_demandeur, entry_list, max_detour):
    result = []
    for e in entry_list:
        if routeInEllipse(point_home_demandeur, point_work_demandeur, e.departure.point,
                          e.arrival.point, max_detour):
            result.append(e)
    return result


# Second filter

def fullRouteFilter(point_home_demandeur, point_work_demandeur, entry_list, max_detour):
    result = []
    for e in entry_list:
        distanceTrajetSimu = distance(e.departure.point, point_home_demandeur) + distance(point_home_demandeur,
                                                                                          point_work_demandeur) + distance(
            point_work_demandeur, e.arrival.point)
        distanceTrajetInit = distance(e.departure.point, e.arrival.point)
        if (distanceTrajetSimu <= distanceTrajetInit + max_detour):
            if not isPresent(e, result):
                result.append(e)
    return result


# Day filter

def dayFilter(day, entry_list):
    result = []
    for e in entry_list:
        if e.day == day:
            if not isPresent(e, result):
                result.append(e)
    return result


#Schedulefilter
#nbhours = temps grossier en détour pour le filtre, arguments may be ints, longs, or floats, and may be positive or negative.

def scheduleFilter(hour, minute, entry_list, nbhours):
    result = []
    s = datetime(100, 1, 1, hour, minute)
    time1 = s + timedelta(hours=nbhours)
    time2 = s + timedelta(hours=-nbhours)
    if time1.time() > time2.time():
        timemax = time1
        timemin = time2
    else:
        timemax = time2
        timemin = time1
    #print('timemax :')
    #print(timemax.time())
    #print('timemin :')
    #print(timemin.time())
    for e in entry_list:
        #print('schedule :')
        #print(e.schedule)
        if timemin.time() <= e.schedule <= timemax.time():
            if not isPresent(e, result):
                result.append(e)
    return result


#Schedulefilter
#Select all the path done between hourmin:minunteMin and hourMax:minuteMax


def scheduleFilterIntervalle(hourMin, minuteMin, hourMax, minuteMax, entry_list):
    result = []
    min = datetime(100, 1, 1, hourMin, minuteMin)
    max = datetime(100, 1, 1, hourMax, minuteMax)

    #print('timemax :')
    #print(max.time())
    #print('timemin :')
    #print(min.time())
    for e in entry_list:
        #print('schedule :')
        #print(e.schedule)
        if min.time() <= e.schedule <= max.time():
            if not isPresent(e, result):
                result.append(e)
    return result


def addHours(tm, hours):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(hours=hours)
    return fulldate.time()


# isPresent : check if x is present in list
def isPresent(x, list):
    result = False
    for e in list:
        if e == x:
            result = True
    return result


# Functions used for filtering the database geometrically

def distance(pos1, pos2):
    """Returns the distance between two 2D points (2-tuples)"""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def pointInEllipse(pos_client, pos1_provider, pos2_provider, max_detour):
    """Returns True if the client's point is inside
    the ellipse associated to provider's starting    and finish points and some spatial detour"""
    return distance(pos_client, pos1_provider) + distance(pos_client, pos2_provider) \
           <= distance(pos1_provider, pos2_provider) + max_detour


def routeInEllipse(pos1_client, pos2_client, pos1_provider, pos2_provider, max_detour):
    """Returns True iff both of client's starting and finish points are inside
    the ellipse associated to provider's starting and finish points and some spatial detour"""
    return pointInEllipse(pos1_client, pos1_provider, pos2_provider, max_detour) \
           & pointInEllipse(pos2_client, pos1_provider, pos2_provider, max_detour)


def calculate_success(current_calendar):
    success_pourcent = 0
    red = 0
    go_list = current_calendar.go.split(',')
    return_list = current_calendar.back.split(',')

    for elem in go_list:
        if elem == "V":
            success_pourcent += 1
            red += 1.00
        if elem == "R":
            red += 1.00

    for elem in return_list:
        if elem == "V":
            success_pourcent += 1
            red += 1.00
        if elem == "R":
            red += 1.00
    if red == 0:
        success_pourcent = 100
    else:
        success_pourcent = success_pourcent / red * 100.0
    return round(success_pourcent, 2)


@staff_member_required
def applicant_search(request, calendar_id):
    try:
        Calendar.objects.get(idCalendar=calendar_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/BO/utilisateurs/?u=demandeur')
    formset_post = formset_factory(ResearchForm2, extra=0)
    if request.method == 'POST':
        if request.POST.get('sauvegarder'):
            pre = request.POST.get('sauvegarder').split("-")
            for i in range(0, int(pre[3])):
                formset = formset_post(request.POST, prefix=str(i) + "-0")
                formset2 = formset_post(request.POST, prefix=str(i) + "-1")
                try:
                    if formset.is_valid():
                        entry = Research.objects.filter(idCalendar=formset[0]['idCalendar'].value,
                                                        streetDeparture__startswith=formset[0]['streetDeparture'].value,
                                                        streetArrival__startswith=formset[0]['streetArrival'].value,
                                                        idPath=formset[0]['idPath'].value).order_by('idResearch')
                        i = 0
                        for i, form in enumerate(formset):
                            if form.is_valid():
                                if entry[i].validated != form.cleaned_data['validated']:
                                    to_modify = entry[i]
                                    to_modify.validated = form.cleaned_data['validated']
                                    to_modify.save()
                except ValidationError:
                    pass
                try:
                    if formset2.is_valid():

                        entry2 = Research.objects.filter(idCalendar=formset2[0]['idCalendar'].value,
                                                         streetDeparture__startswith=formset2[0][
                                                             'streetDeparture'].value,
                                                         streetArrival__startswith=formset2[0]['streetArrival'].value,
                                                         idPath=formset2[0]['idPath'].value).order_by('idResearch')

                        j = 0
                        for j, form2 in enumerate(formset2):
                            if form2.is_valid():
                                if entry2[j].validated != form2.cleaned_data['validated']:
                                    to_modify = entry2[j]
                                    to_modify.validated = form2.cleaned_data['validated']
                                    to_modify.save()
                except ValidationError:
                    pass
        if request.POST.get("supprimer"):
            pre = request.POST.get('supprimer').split("-")
            if int(pre[1]) == 0:
                formset = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])
                formset2 = []
            else:
                if int(pre[2]) == 1:
                    formset2 = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])
                    formset = []
                else:
                    formset = formset_post(request.POST, prefix=pre[0] + "-0")
                    formset2 = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])

            if formset and formset.is_valid():
                Research.objects.filter(idCalendar=formset[0]['idCalendar'].value,
                                        streetDeparture__startswith=formset[0]['streetDeparture'].value,
                                        streetArrival__startswith=formset[0]['streetArrival'].value,
                                        idPath=formset[0]['idPath'].value).order_by('idResearch').delete()

            if formset2 and formset2.is_valid():
                Research.objects.filter(idCalendar=formset2[0]['idCalendar'].value,
                                        streetDeparture__startswith=formset2[0]['streetDeparture'].value,
                                        streetArrival__startswith=formset2[0]['streetArrival'].value,
                                        idPath=formset2[0]['idPath'].value).order_by('idResearch').delete()
        '''if request.POST.get("archiver"):
            pre = request.POST.get('archiver').split("-")
            formset_post_historic = formset_factory(HistoricForm, extra=0)

            if int(pre[1]) == 0:
                formset = formset_post_historic(request.POST, prefix=pre[0] + "-" + pre[1])
                formset2 = []
            else:
                if int(pre[2]) == 1:
                    formset2 = formset_post_historic(request.POST, prefix=pre[0] + "-" + pre[1])
                    formset = []
                else:
                    formset = formset_post_historic(request.POST, prefix=pre[0] + "-0")
                    formset2 = formset_post_historic(request.POST, prefix=pre[0] + "-" + pre[1])

            if formset and formset.is_valid():
                for form in formset:
                    if form.is_valid() and form['validated'].data:
                        form.save()

            if formset2 and formset2.is_valid():
                for form in formset2:
                    if form.is_valid() and form['validated'].data:
                        form.save()
            # delete after archive
            if int(pre[1]) == 0:
                formset = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])
                formset2 = []
            else:
                if int(pre[2]) == 1:
                    formset2 = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])
                    formset = []
                else:
                    formset = formset_post(request.POST, prefix=pre[0] + "-0")
                    formset2 = formset_post(request.POST, prefix=pre[0] + "-" + pre[1])

            if formset and formset.is_valid():
                Research.objects.filter(idCalendar=formset[0]['idCalendar'].value,
                                        streetDeparture__startswith=formset[0]['streetDeparture'].value,
                                        streetArrival__startswith=formset[0]['streetArrival'].value,
                                        idPath=formset[0]['idPath'].value).order_by('idResearch').delete(),

            if formset2 and formset2.is_valid():
                Research.objects.filter(idCalendar=formset2[0]['idCalendar'].value,
                                        streetDeparture__startswith=formset2[0]['streetDeparture'].value,
                                        streetArrival__startswith=formset2[0]['streetArrival'].value,
                                        idPath=formset2[0]['idPath'].value).order_by('idResearch').delete()'''

        if request.POST.get("savecalendar"):
            current_calendar = Calendar.objects.get(idCalendar=calendar_id)
            go_list = current_calendar.go.split(',')
            return_list = current_calendar.back.split(',')
            go_list_on = []
            return_list_on = []
            new_go_string = ""
            new_return_string = ""
            for i in range(0, 14):
                elem = request.POST.get("go_" + str(i))
                elem2 = request.POST.get("return_" + str(i))
                if elem is not None:
                    go_list_on.append(i)
                if elem2 is not None:
                    return_list_on.append(i)
                if elem is None and go_list[i] == "V":
                    go_list[i] = "R"
                if elem2 is None and return_list[i] == "V":
                    return_list[i] = "R"

            for i in go_list_on:
                go_list[i] = "V"
            for i, v in enumerate(go_list):
                if i == 0:
                    new_go_string = new_go_string + v
                else:
                    new_go_string = new_go_string + "," + v
            current_calendar = Calendar.objects.filter(idCalendar=calendar_id)
            current_calendar.update(go=new_go_string)

            for j in return_list_on:
                return_list[j] = "V"
            for j, v in enumerate(return_list):
                if j == 0:
                    new_return_string = new_return_string + v
                else:
                    new_return_string = new_return_string + "," + v
            current_calendar.update(back=new_return_string)
        if request.POST.get("archiveCalendar"):
            current_calendar = Calendar.objects.get(idCalendar=calendar_id)
            go_list = current_calendar.go.split(',')
            return_list = current_calendar.back.split(',')
            go_list_on = []
            return_list_on = []
            new_go_string = ""
            new_return_string = ""
            for i in range(0, 14):
                elem = request.POST.get("go_" + str(i))
                elem2 = request.POST.get("return_" + str(i))
                if elem is not None:
                    go_list_on.append(i)
                if elem2 is not None:
                    return_list_on.append(i)
                if elem is None and go_list[i] == "V":
                    go_list[i] = "R"
                if elem2 is None and return_list[i] == "V":
                    return_list[i] = "R"

            for i in go_list_on:
                go_list[i] = "V"
            for i, v in enumerate(go_list):
                if i == 0:
                    new_go_string = new_go_string + v
                else:
                    new_go_string = new_go_string + "," + v
            current_calendar = Calendar.objects.filter(idCalendar=calendar_id)
            current_calendar.update(go=new_go_string)

            for j in return_list_on:
                return_list[j] = "V"
            for j, v in enumerate(return_list):
                if j == 0:
                    new_return_string = new_return_string + v
                else:
                    new_return_string = new_return_string + "," + v
            current_calendar.update(back=new_return_string)

            #update success %
            current_calendar = Calendar.objects.get(idCalendar=calendar_id)
            success_pourcent = calculate_success(current_calendar)


            #archive after save
            pourcentage = success_pourcent
            idApplicant = current_calendar.idApplicant
            dateBeginning = current_calendar.dateBeginningGo
            scheduleBeginningGo = current_calendar.scheduleBeginningGo
            scheduleBeginningBack = current_calendar.scheduleBeginningBack
            go = current_calendar.go
            back = current_calendar.back
            possibleMeetingSpot = current_calendar.possibleMeetingSpot
            streetHome = current_calendar.streetHome
            streetWork = current_calendar.streetWork
            transportIssue = current_calendar.transportIssue,
            comment = request.POST.get('comment')
            histocal = HistoricCalendar.objects.create(pourcentage=pourcentage, idApplicant=idApplicant,
                                        dateBeginning=dateBeginning, scheduleBeginningGo=scheduleBeginningGo,
                                        scheduleBeginningBack=scheduleBeginningBack, go=go, back=back,
                                        streetHome=streetHome, streetWork=streetWork,
                                        possibleMeetingSpot=possibleMeetingSpot,transportIssue=transportIssue,
                                        comment=comment)
            #archive validated researchs of this calendar
            starting_date = current_calendar.dateBeginningGo
            researchs = Research.objects.filter(idCalendar=current_calendar.pk).order_by('idResearch')
            if researchs:
                i = 0
                idPath = researchs[0].idPath.idPath
                for r in researchs:
                    if r.idPath.idPath != idPath:
                        i = 0
                        idPath = r.idPath.idPath
                    date = starting_date + timedelta(days=i)
                    r.archive(date, histocal)
                    i += 1

            #delete
            current_calendar.delete()
            return HttpResponseRedirect('/BO/utilisateurs/d/' + str(idApplicant.idApplicant))
    #On récupère l'applicant courant pour rappeler son nom et prénom en début de page.
    current_calendar = Calendar.objects.get(idCalendar=calendar_id)
    name = current_calendar.idApplicant.idUser.name
    firstname = current_calendar.idApplicant.idUser.firstname

    success_pourcent = calculate_success(current_calendar)

    go_list = current_calendar.go.split(',')
    return_list = current_calendar.back.split(',')

    departure = current_calendar.streetHome.replace(', France', '')
    back = current_calendar.streetWork.replace(', France', '')

    list_res = []
    #On récupère toutes les données de Research correspondant à cet applicant.
    all_calendar_search = Research.objects.filter(idCalendar=calendar_id).order_by('idResearch')

    dict_days_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                         'sunday': 6}

    all_path_in_calendar_research = all_calendar_search.values('idPath')
    all_path = []
    #On supprime les doublons
    for value in all_path_in_calendar_research:
        if value not in all_path:
            all_path.append(value)
    all_providers = []
    for path in all_path:
        for p in Path.objects.filter(idPath=path.get('idPath')).select_related('idProvider'):
            id = p.idProvider.idProvider
            if id not in all_providers:
                all_providers.append(id)

    #starting_day = dict_days_of_week[all_results_for_one_research_provider[0].idPath.day]
    mydate = current_calendar.dateBeginningGo
    days_list = create_daysNum_list(mydate, 14)
    days_list_name = create_daysName_list(mydate.weekday())

    counter_provider = 0
    for provider in all_providers:
        provider_for_list = []
        list_form = []
        list_form2 = []
        all_results_for_one_provider = all_calendar_search.filter(idPath__idProvider=provider).select_related()

        all_results_go = all_results_for_one_provider.filter(isGo=True).order_by('idResearch')
        all_results_return = all_results_for_one_provider.filter(isGo=False).order_by('idResearch')

        counter1 = 0
        for result in all_results_go:
            provider_name = result.idPath.idProvider.idUser.name
            providerPhone = result.idPath.idProvider.idUser.phone
            provider_firstname = result.idPath.idProvider.idUser.firstname
            provider = provider_firstname + " " + provider_name
            providerId = result.idPath.idProvider.idProvider
            firstdate = current_calendar.dateBeginningBack
            date = addDay(firstdate, counter1)

            list_form.append({'providerName': provider,
                              'providerPhone': providerPhone,
                              'providerId': providerId,
                              'date': date,
                              'idCalendar': result.idCalendar,
                              'idPath': result.idPath,
                              'detour': result.detour,
                              'detourkm': result.detourkm,
                              'streetDeparture': result.streetDeparture.replace(', France', ''),
                              'streetArrival': result.streetArrival.replace(', France', ''),
                              'available': result.available,
                              'validated': result.validated,
                              'isGo': result.isGo, })

            counter1 += 1
        applicant_research_formset = formset_factory(ResearchForm2, extra=0)
        if list_form:
            formset_go = applicant_research_formset(initial=list_form, prefix=str(counter_provider) + "-0")

        counter2 = 0
        for result in all_results_return:
            provider_name = result.idPath.idProvider.idUser.name
            provider_firstname = result.idPath.idProvider.idUser.firstname
            provider = provider_name + " " + provider_firstname
            providerId = result.idPath.idProvider.idProvider
            print providerId
            firstdate = current_calendar.dateBeginningBack
            date = addDay(firstdate, counter2)

            list_form2.append({'providerName': provider,
                               'providerId': providerId,
                               'date': date,
                               'idCalendar': result.idCalendar,
                               'idPath': result.idPath,
                               'detour': result.detour,
                               'detourkm': result.detourkm,
                               'streetDeparture': result.streetDeparture.replace(', France', ''),
                               'streetArrival': result.streetArrival.replace(', France', ''),
                               'available': result.available,
                               'validated': result.validated,
                               'isGo': result.isGo, })
            counter2 += 1

        if list_form2:
            formset_return = applicant_research_formset(initial=list_form2, prefix=str(counter_provider) + "-1")

        if list_form:
            provider_for_list.append(formset_go)
        if list_form2:
            provider_for_list.append(formset_return)

        list_res.append(provider_for_list)

        counter_provider += 1
    options_0 = u'<option selected hidden value=""></option><option value="Abandon du demandeur">Abandon du demandeur</option><option value="Abandon de la structure accompagnante">Abandon de la structure accompagnante</option><option value="Pas de solution trouvée">Pas de solution trouvée</option><option value="Le demandeur a trouvé une autre solution">Le demandeur a trouvé une autre solution</option><option value="Hors cadre EHOP-solidaires">Hors cadre EHOP-solidaires</option>'.encode("utf-8")
    options = u'<option selected hidden value=""></option><option value="Deuxième solution trouvée par ses propres moyens">Deuxième solution trouvée par ses propres moyens</option><option value="Trajet complété par transports en commun">Trajet complété par transports en commun</option><option value="Pas de retour du demandeur">Pas de retour du demandeur</option>'
    variables = {'list_res': list_res,
                 'firstname': firstname,
                 'name': name,
                 'go_list': go_list,
                 'return_list': return_list,
                 'departure': departure,
                 'back': back,
                 'days_list': days_list,
                 'mydate': mydate,
                 'success': success_pourcent,
                 'days_list_name': days_list_name,
                 'applicant': current_calendar.idApplicant,
                 'options':options,
                 'options_0':options_0}

    return render(request, 'admin/demandeur_recherches.html', variables)