# -*- coding: utf-8 -*-

# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import formset_factory
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User as django_user
from django.core.mail import EmailMessage
from django.forms.models import modelformset_factory
from django.forms.formsets import INITIAL_FORM_COUNT
from django.core.exceptions import ObjectDoesNotExist
from forms import *
from models import *
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import math
import datetime
from datetime import timedelta


def home(request):
    return render(request, 'ehopSolidaire_providers_register/accueil.html', {})


def login_view(request):
    msg = ""
    if request.method == 'POST':
        email_form = request.POST.get('mail', None)
        password_form = request.POST.get('password', None)
        auth = EmailAuthBackend()
        user = auth.authenticate2(username=email_form, password=password_form)
        # normal users
        if user is not None:
            u = auth.authenticate(username=email_form, password=password_form)
            if not u:
                user_name = User.objects.filter(mail=email_form).first()
                u = django_user.objects.create_user(email_form, email_form, password_form)
                django_User.objects.filter(email=email_form).update(first_name=user_name.firstname, last_name=user_name.name)
            if u.is_active:
                u.backend = 'django.contrib.auth.backends.ModelBackend'
                django_login(request, u)
                User.objects.filter(idUser=user.idUser.idUser).update(dateLastConnection=datetime.datetime.today())
                return HttpResponseRedirect('/profil/')
        # superusers
        else:
            user2 = auth.authenticate(username=email_form, password=password_form)
            if user2 is not None:
                if user2.is_active:
                    user2.backend = 'django.contrib.auth.backends.ModelBackend'
                    django_login(request, user2)
                    return HttpResponseRedirect('/profil/')
            else:
                msg = "L'adresse email ou le mot de passe que vous avez entré n'est pas valide"
        messages.error(request, msg)
        return HttpResponseRedirect('/connexion/')
    else:
        email_form = LoginForm()
        password_form = ProviderRegisterForm()
    return render(request, 'ehopSolidaire_providers_register/connexion.html', {'email_form': email_form,
                                                                               'password_form': password_form})


def disconnected(request):
    django_logout(request)
    request.session.flush()
    return HttpResponseRedirect('/accueil/')


#Méthode pour le module 'mot de passe oublié' 
def forgotten(request):
    msg = ""
    msg2 = ""
    if request.method == 'POST':
        email_form = request.POST.get('mail', None)
        auth = EmailAuthBackend()
        user = auth.auth_email(username=email_form)
        if user is not None:
            new_password = django_user.objects.make_random_password()
            message = "Votre nouveau mot de passe sur le site www.ehop-solidaires.fr est : " + new_password + \
                      ".\n\nCordialement,\nL'Equipe d'Ehop, Solidaires !"
            send_mail('Ehop-Solidaires - Mot de passe oublié', message, 'noreply@ehop-solidaires.fr', [email_form])
            user.password = make_password(new_password)
            user.save()
            try:
                django_u = auth.auth_email2(username=email_form)
            except ObjectDoesNotExist:
                django_u = None
            if django_u is not None:
                django_u.set_password(new_password)
                django_u.save()
            else:
                user_name = User.objects.filter(mail=email_form).first()
                django_user.objects.create_user(user_name.name, email_form, new_password)
                django_User.objects.filter(email=email_form).update(first_name=user_name.firstname,
                                                                                 last_name=user_name.name)
            msg2 = "Le nouveau mot de passe a été envoyé avec succès à l'adresse renseignée !"
        else:
            msg = "L'adresse email que vous avez entré n'existe pas dans la base de données offreurs."
        messages.error(request, msg)
        messages.success(request, msg2)
        return HttpResponseRedirect('/mdp-oublie/')
    else:
        email_form = LoginForm()
    return render(request, 'ehopSolidaire_providers_register/mdp-oublie.html', {'email_form': email_form})


def applicant(request):
    counter = Provider.objects.count()+10
    return render(request, 'ehopSolidaire_providers_register/demandeur.html', {'counter': counter})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        msg = msg2 = ""
        if form.is_valid():
            msg = "Votre message à bien été envoyé, nous vous contacterons dès que possible."
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phone = form.cleaned_data['phone']
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            goalOfApplication = form.cleaned_data['goalOfApplication']
            if goalOfApplication != '':
                goalOfApplication = "\nBut de la demande: "+goalOfApplication
            yearOfBirth = form.cleaned_data['yearOfBirth']
            if yearOfBirth != '':
                yearOfBirth = u"\nAnnée de naissance: "+yearOfBirth
            message = form.cleaned_data['message']
            message = message.replace(u"Merci de compléter les champs suivants pour toute demande.","")
            fullmail = "Nom: " + firstname + u"\nPrénom: " + lastname + yearOfBirth + u"\nTéléphone: " + phone + "\nEmail: " + sender \
                       + goalOfApplication + "\nMessage: " + message
            subjectMail = "[Contact] " + subject + ": " + lastname
            send_mail(subjectMail, fullmail, sender, [settings.EMAIL_CONTACT])
        else:
            msg2 = "Il y a eu une erreur lors de l'envoi de votre message."
            msg = form.errors
        messages.error(request, msg2)
        messages.success(request, msg)
    init_message = "Merci de compléter les champs suivants pour toute demande. \n" \
                   "Trajet(départ-arrivée) : \n\n" \
                   "Horaires(arrivée-départ) : \n\n" \
                   "Date de début de covoiturage : \n\n" \
                   "Durée du covoiturage demandé : \n\n" \
                   "Problème de transport rencontré (ex: voiture en panne, pas de permis, ...) :\n"
    form = ContactForm(initial={'message':init_message})
    return render(request, 'ehopSolidaire_providers_register/contact.html', {'form': form,'init_message':init_message.replace('\n','²')})


def submit(request):
    return render(request, 'ehopSolidaire_providers_register/termine.html', {})


def howwork(request):
    return render(request, 'ehopSolidaire_providers_register/fonctionnement.html', {})


def project(request):
    return render(request, 'ehopSolidaire_providers_register/projet.html', {})


def formulaire(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect("/profil/")
    path_departure_register_form_set = formset_factory(PathDepartureRegisterForm)
    path_arrival_register_form_set = formset_factory(PathArrivalRegisterForm)
    msg = ""

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        provider_form = ProviderRegisterForm(request.POST)
        address_home_form = AddressRegisterForm(request.POST, prefix="home")
        address_work_form = AddressRegisterFormWork(request.POST, prefix="work")
        path_departure_register_formset = path_departure_register_form_set(request.POST, prefix="departure")
        path_arrival_register_formset = path_arrival_register_form_set(request.POST, prefix="arrival")
        startingweek = request.POST.get("startingWeek", "")
        isNonFixe = request.POST.get('checkNonFixe') != None
        if isNonFixe:
            list_days_selected = request.POST.get('listDaysSelected').split('_')
            list_days_selected = [x for x in list_days_selected if x] # remove empty strings
            print list_days_selected
            paths = list()
            for day in list_days_selected:
                path_go = {}
                path_back = {}
                path_go['schedule'] = request.POST.get('datetime_'+day+'_0_0')
                path_go['schedule2'] = request.POST.get('datetime_'+day+'_0_1')
                path_go['day'] = getDayName(day)
                path_go['type'] = 4
                path_go['startingWeek'] = 0
                path_go['weekNumber'] = 'A'
                path_back['schedule'] = request.POST.get('datetime_'+day+'_1_0')
                path_back['schedule'] = request.POST.get('datetime_'+day+'_1_1')
                path_back['day'] = getDayName(day)
                path_back['type'] = 4
                path_back['startingWeek'] = 0
                path_back['weekNumber'] = 'A'
                paths.append(path_go)
                paths.append(path_back)
            print paths
            addresses = list()
            for i in range(1,6):
                address = {}
                if request.POST.get('work'+str(i)+'-street'):
                    address['street'] = request.POST.get('work'+str(i)+'-street')
                    address['point'] = latlng_to_point(request.POST.get('work'+str(i)+'-latlng'))
                    addresses.append(address)
            print addresses

        if not user_form.is_valid():
            u = user_form.instance
            if u.mail == "":
                msg = "Vous n'avez pas entré d'adresse mail."
            elif u.mail != "":
                msg = "Cette adresse mail est déjà utilisée."
            else:
                msg = "Il existe une erreur dans les informations que vous avez entrées, veuillez recommencer."
        elif not isNonFixe and not address_home_form.is_valid():
            print "home form : "
            adh = address_home_form.instance
            print(address_home_form.cleaned_data)
            # msg = address_home_form.errors
            msg = "Il existe une erreur dans votre adresse de domicile"
        elif not isNonFixe and not address_work_form.is_valid():
            print "work form : "
            adw = address_work_form.instance
            print(address_work_form.cleaned_data)
            msg = "Il existe une erreur dans votre adresse de travail"
        elif not provider_form.is_valid():
            print "provider form : "
            print provider_form.cleaned_data
            msg = "Il existe une erreur dans les informations que vous avez entrées, veuillez recommencer."
            msg = provider_form
        elif not path_arrival_register_formset.is_valid():
            print "prise de service : "
            for arrival_form in path_arrival_register_formset:
                print arrival_form.cleaned_data
            msg = "Il existe une erreur dans le planning que vous avez entré, veuillez recommencer."
        elif not path_departure_register_formset.is_valid():
            print "fin de service : "
            for departure_form in path_departure_register_formset:
                print departure_form.cleaned_data
            msg = "Il existe une erreur dans le planning que vous avez entré, veuillez recommencer."
        else:
            address_home = address_home_form.save(commit=False)
            address_home.point = address_home_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad = Address.objects.filter(point=address_home.point)
            if queryad:
                #On recupere l'adresse deja stocke
                address_home=queryad[0]
            else:
                #sinon on sauvegarde la nouvelle
                address_home.zipCode=address_home_form.cleaned_data['zipCode']
                address_home.city=address_home_form.cleaned_data['city']
                address_home.save()
            address_work = address_work_form.save(commit=False)
            address_work.point = address_work_form.cleaned_data['point']
            #Requete qui recupere les adresses identiques si elles existent
            queryad=Address.objects.filter(point=address_work.point)
            if queryad:
                #Au cas ou plusieurs adresse identique se trouveraient deja dans la bdd
                address_work=queryad[0]
            else :
                #sauvegarde de la nouvelle adresse
                address_work.zipCode=address_work_form.cleaned_data['zipCode']
                address_work.city=address_work_form.cleaned_data['city']
                address_work.save()

            user_form.instance.idHomeAddress_id = address_home.pk
            user_form.instance.idWorkAddress_id = address_work.pk
            user = user_form.save()
            provider_form.instance.idUser_id = user.pk
            provider_form.instance.password = make_password(provider_form.cleaned_data['password'])
            provider = provider_form.save()
            for departure_form in path_departure_register_formset:
                departure_form.instance.idProvider_id = provider.pk
                departure_form.instance.departure_id = address_home.pk
                departure_form.instance.arrival_id = address_work.pk
                departure_form.instance.startingWeek = startingweek
                if departure_form.is_valid() and departure_form.has_changed():
                    departure_form.save()
            for arrival_form in path_arrival_register_formset:
                arrival_form.instance.idProvider_id = provider.pk
                arrival_form.instance.departure_id = address_work.pk
                arrival_form.instance.arrival_id = address_home.pk
                arrival_form.instance.startingWeek = startingweek
                if arrival_form.is_valid() and arrival_form.has_changed():
                    arrival_form.save()


            #Envoi du mail automatique :
            html_content = render_to_string('ehopSolidaire_providers_register/mail_confirmation_inscription.html')
            text_content = strip_tags(html_content)
            u = user_form.instance
            msg = EmailMultiAlternatives("Ehop-Solidaires - Confirmation d'inscription", text_content, settings.EMAIL_HOST_USER, [u.mail])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/termine/')
    else:
        address_home_form = AddressRegisterForm(prefix="home")
        address_work_form = AddressRegisterFormWork(prefix="work")
        user_form = UserRegisterForm()
        provider_form = ProviderRegisterForm()

        path_departure_register_formset = path_departure_register_form_set(prefix="departure")
        path_arrival_register_formset = path_arrival_register_form_set(prefix="arrival")

    messages.error(request, msg)
    return render(request, 'ehopSolidaire_providers_register/offreur.html', {
        'address_home_form': address_home_form,
        'address_work_form': address_work_form,
        'user_form': user_form,
        'provider_form': provider_form,
        'path_departure_register_formset': path_departure_register_formset,
        'path_arrival_register_formset': path_arrival_register_formset,
        'companiesList': getCompaniesList()
        })


def latlng_to_point(latlng):
    coord = latlng.replace('(', '')
    if coord == "" or coord == "undefined":
        return -1
    coord = coord.replace(')', '')
    coordtab = coord.split(',')
    return 'POINT(%f %f)' % (float(coordtab[0]), float(coordtab[1]))


def getDayName(day):
    if day == "0":
        return 'monday'
    if day == "1":
        return 'tuesday'
    if day == "2":
        return 'wednesday'
    if day == "3":
        return 'thursday'
    if day == "4":
        return 'friday'
    if day == "5":
        return 'saturday'
    if day == "6":
        return 'sunday'

def getCompaniesList():
    return Companies.objects.values_list('name',flat=True)

'''
    Modifie le mot de passe d'un utilisateur
'''

#@login_required(login_url='/connexion/')
def change_password(request):
    #message d'erreur
    msg = ''

    #on recupere l'utilisateur connecte
    current_user_django = request.user
    current_user = User.objects.get(mail=current_user_django.email)
    current_provider = Provider.objects.get(idUser=current_user)

    if request.method == 'POST':
        mdp_form = newMdpForm(request.POST)
        if not mdp_form.is_valid():
            msg = "une erreur dans le formulaire"
            messages.add_message(request, messages.ERROR, msg)
        else:
            #ancien mdp rentrer par lutilisateur
            in_old_mdp = mdp_form.cleaned_data['oldmdp']
            in_new_mdp = mdp_form.cleaned_data['newmdp1']
            if check_password(in_old_mdp,current_user_django.password):
                current_provider.password = make_password(in_new_mdp)
                current_provider.save()
                current_user_django.password = current_provider.password
                current_user_django.save()
                msg = 'Votre mot de passe a été modifié'
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = 'Ancien mot de passe incorrect'
                messages.add_message(request, messages.ERROR, msg)

    mdp_form = newMdpForm()
    return render(request,
                  'ehopSolidaire_providers_register/change_mdp.html', {'mdp_form': mdp_form})



def sitemap(request):
    return render(request, 'sitemap.xml', {})


def conditions(request):
    return render(request, 'ehopSolidaire_providers_register/conditions.html', {})


@login_required(login_url='/connexion/')
def profil(request):
    #message d'erreur
    msg = ''

    #on recupere l'utilisateur connecte
    current_user_django = request.user
    try:
        current_user = User.objects.get(mail=current_user_django.email)
    except User.DoesNotExist:
        msg = 'Vous n\'avez pas de compte Offreur utilisant le mail: '+current_user_django.email
        messages.error(request, msg)
        return HttpResponseRedirect('/BO/')

    current_provider = Provider.objects.get(idUser=current_user)

    path_departure_register_form_set = formset_factory(PathDepartureRegisterForm)
    path_arrival_register_form_set = formset_factory(PathArrivalRegisterForm)

    if request.method == 'POST':
        if request.POST.get('supprimer'):
            django_user.objects.get(Q(username=current_user.mail) | Q(email=current_user.mail)).delete()
            from ehop.admin.charts import get_intercommunity, get_intercommunities
            intercoms = get_intercommunities()
            Deletion.objects.create(dateDelete=datetime.now(),dateRegister=current_user.dateRegister,
                                    type="provider", reason=request.POST.get('supprimer'),
                                    homeIntercommunity=get_intercommunity(intercoms,current_user.idHomeAddress.street),
                                    workIntercommunity=get_intercommunity(intercoms,current_user.idWorkAddress.street))
            current_user.delete()
            django_logout(request)
            request.session.flush()
            return HttpResponseRedirect('/accueil/')
        startingWeek = request.POST.get("startingWeek", "")
        user_form = TestUserRegisterForm(request.POST, instance=current_user)
        provider_form = ProviderForm2(request.POST, instance=current_provider)
        address_home_form = AddressRegisterForm(request.POST, prefix="home")
        address_work_form = AddressRegisterFormWork(request.POST, prefix="work")
        path_departure_register_formset = path_departure_register_form_set(request.POST, prefix="departure")
        path_arrival_register_formset = path_arrival_register_form_set(request.POST, prefix="arrival")
        if not user_form.is_valid():
            u = user_form.instance
            if u.mail == "":
                msg = "Vous  n'avez pas entre d'adresse mail."
            elif u.mail != "":
                msg = "Cette adresse mail est déjà utilisée."
            else:
                msg = "Il existe une erreur dans les informations que vous avez entrees, veuillez recommencer."
            messages.add_message(request, messages.ERROR, msg)
        elif not address_home_form.is_valid():
            msg = "Il existe une erreur dans l'adresse de depart"
            messages.add_message(request, messages.ERROR, msg)
        elif not address_work_form.is_valid():
            msg = "Il existe une erreur dans l'adresse de arrivee"
            messages.add_message(request, messages.ERROR, msg)
        elif not path_departure_register_formset.is_valid():
            msg = "Il existe une erreur dans vos horaires"
            messages.add_message(request, messages.ERROR, msg)
        elif not path_arrival_register_formset.is_valid():
            msg = "Il existe une erreur dans vos horaires"
            messages.add_message(request, messages.ERROR, msg)
        elif not provider_form.is_valid():
            msg = "Il existe une erreur dans votre nom d'entreprise"
            messages.add_message(request, messages.ERROR, msg)
        else:
            Provider.objects.filter(idProvider=current_provider.idProvider).update(company=provider_form.cleaned_data['company'],
                                                                                   howKnowledge=provider_form.cleaned_data['howKnowledge'])
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

            #on modifie le mail dans la table django
            current_user_django.email = current_user.mail
            current_user_django.save()

            #on supprimme les anciennes horaires
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

            msg = "Les informations ont correctement été modifiées."
            messages.add_message(request, messages.SUCCESS, msg)

    user_form = TestUserRegisterForm(initial={'name': current_user.name, 'firstname':current_user.firstname,'city':current_user.city,'zipCode':current_user.zipCode,'mail':current_user.mail,'sex':current_user.sex,'phone':current_user.phone})
    address_home_form = AddressRegisterForm(initial={'street': current_user.idHomeAddress.street},prefix="home")
    address_work_form = AddressRegisterFormWork(initial={'street': current_user.idWorkAddress.street},prefix="work")
    provider_form = ProviderForm2(initial={'company':current_provider.company, 'howKnowledge': current_provider.howKnowledge})

    #on recupere les trajets
    provider = Provider.objects.filter(idUser=current_user)
    paths = Path.objects.filter(idProvider=current_provider).order_by('idPath')

    provider = Provider.objects.filter(idUser=current_user)
    path_departure_register_formset = path_departure_register_form_set(prefix="departure")
    path_arrival_register_formset = path_arrival_register_form_set(prefix="arrival")

    return render(request, 'ehopSolidaire_providers_register/profil.html', {
        'user_form': user_form,
        'address_home_form': address_home_form,
        'address_work_form': address_work_form,
        'provider_form': provider_form,
        'path_departure_register_formset': path_departure_register_formset,
        'path_arrival_register_formset': path_arrival_register_formset,
        'paths': paths,
        'companiesList': getCompaniesList()
        })
           
           

