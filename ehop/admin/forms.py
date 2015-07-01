#!/usr/bin/python
# -*- coding: UTF-8 -*-

# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from ehopSolidaire_providers_register.models import *
from django import forms
import datetime


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={'label': 'Nom','required': 'required','readonly' : 'true'}),
            'firstname': forms.TextInput(attrs={'label': 'Prenom','required': 'required','readonly' : 'true'}),
            'city': forms.TextInput(attrs={'label': 'Ville','required': 'required','readonly' : 'true'}),
            'sex': forms.RadioSelect(attrs={'required': 'required'}),
            'zipCode': forms.TextInput(attrs={'label': 'Code Postal','maxlength': '5', 'aria-invalid': 'true','required': 'required', 'readonly' : 'true'}),
            'mail': forms.TextInput(attrs={'label': 'Email','aria-invalid': 'true', 'required': 'required','readonly' : 'true'}),
            'phone': forms.TextInput(attrs={'label': 'Telephone ' , 'maxlength': '10', 'aria-invalid': 'true', 'required': 'required','readonly' : 'true'}),
            }
        exclude = ['idHomeAddress', 'idWorkAddress']


class ProviderRegisterForm(forms.ModelForm):
    class Meta:
        model = Provider
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'password', 'required': 'required'}),
            }
        exclude = ['idUser']


class ApplicantRegisterForm(forms.ModelForm):
    class Meta:
        model = Applicant
        carringAgencyCHOICES = (('', ''), ('Pôle Emploi', 'Pôle Emploi'), ('MEIF', 'MEIF'), ('Mission Locale', 'Mission Locale'),
                                ('PAE', 'PAE'), ('ALI', 'ALI'), ('Demande personnelle', 'Demande personnelle'),
                                ('Association d\'insertion','Association d\'insertion'))
        goalOfApplicationCHOICES = (('', ''), ('Entretien d\'embauche','Entretien d\'embauche'), ('Formation', 'Formation'),
                                    ('Apprentissage', 'Apprentissage'), ('Intérim', 'Intérim'),
                                    ('CDI', 'CDI'), ('CDD', 'CDD'),
                                    ('Stage', 'Stage'), ('Autre', 'Autre'))
        scheduleTypeCHOICES = (('', ''), ('Horaires fixes en journée', 'Horaires fixes en journée'),
                               ('Horaires de nuit', 'Horaires de nuit'), ('3X8', '3X8'),
                               ('2X8', '2X8'), ('Autre', 'Autre'))
        yearOfBirthCHOICES = (tuple((str(n), str(n)) for n in range(1900, datetime.datetime.now().year - 15))+(('',''),))[::-1]
        widgets = {
            'carringAgency': forms.Select(choices=carringAgencyCHOICES),
            'accompMail': forms.EmailInput(),
            'goalOfApplication': forms.Select(choices=goalOfApplicationCHOICES),
            'yearOfBirth': forms.Select(choices=yearOfBirthCHOICES, attrs={'required':'required'}),
            'scheduleType': forms.Select(choices=scheduleTypeCHOICES),
            }
        exclude = ['idApplicant', 'idUser']


    def clean_identNum(self):
        return self.cleaned_data['identNum'] or None


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar

        today = datetime.date.today()
        if(today.day < 10):
            day = '0%d'%today.day
        else:
            day = '%d'%today.day
        if(today.month < 10):
            month = '0%d'%today.month
        else:
            month = '%d'%today.month
        year = '%d'%today.year
        today = day+'/'+month+'/'+year

        widgets = {
            'dateBeginningGo': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'dp', 'value': today}),
            'scheduleBeginningGo': forms.TextInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm', 'value': '08:00'}),
            'scheduleBeginningBack': forms.TextInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm', 'value': '18:00'}),
        }
        exclude = ['idApplicant', 'dateBeginningBack', 'go', 'back', 'streetHome', 'streetWork']


class CalendarModifyForm(forms.ModelForm):
    class Meta:
        model = Calendar
        widgets = {
            'dateBeginningGo': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'class': 'dp'}),
            'scheduleBeginningGo': forms.TextInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm'}),
            'scheduleBeginningBack': forms.TextInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm'}),
        }
        exclude = ['idApplicant', 'dateBeginningBack', 'go', 'back']

class CalendarFormDisplay(forms.ModelForm):
    listGo = forms.CharField(required=False)
    listBack = forms.CharField(required=False)
    listDaysName = forms.CharField(required=False)
    listDaysNum = forms.CharField(required=False)
    address_home = forms.CharField(required=False)
    address_work = forms.CharField(required=False)
    idCalendar = forms.CharField(required=False)
    success = forms.CharField(required=False)
    scheduleBeginningGo = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    scheduleBeginningBack = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    dateBeginningGo = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    streetHome = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    streetWork = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Calendar

        widgets={
            'transportIssue': forms.TextInput(attrs={'readonly':'readonly'}),
            'possibleMeetingSpot': forms.TextInput(attrs={'readonly':'readonly'})
        }
        exclude = ['idApplicant', 'dateBeginningBack', 'go', 'back']

class UserRegisterForm2(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={'required': 'required'}),
            'firstname': forms.TextInput(attrs={'required': 'required'}),
            'sex': forms.RadioSelect(attrs={'required': 'required'}),
            'mail': forms.EmailInput(attrs={'aria-invalid': 'true', 'pattern': 'email'}),
            'phone': forms.TextInput(attrs={'maxlength': '10', 'aria-invalid': 'true', 'pattern': 'phone', 'required': 'required'}),
            }
        exclude = ['idHomeAddress', 'idWorkAddress', 'zipCode', 'city']

    def clean_mail(self):
        return self.cleaned_data['mail'] or None


class TestUserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={}),
            'firstname': forms.TextInput(attrs={}),
            'mail': forms.EmailInput(attrs={'aria-invalid': 'true'}),
            'city': forms.TextInput(attrs={'aria-invalid': 'true'}),
            'zipCode': forms.TextInput(attrs={'aria-invalid': 'true'}),
            'phone': forms.TextInput(attrs={'maxlength': '10', 'aria-invalid': 'true'}),
            }
        exclude = ['idHomeAddress', 'idWorkAddress', 'sex']


class ResearchForm(forms.Form):
    departure_latlng = forms.CharField(widget=forms.HiddenInput(), required=False,)
    departure = forms.CharField(widget=forms.TextInput(attrs={'class': 'field',
                                                              'placeholder': 'Indiquez un lieu',
                                                              'autocomplete': 'on', 'required': 'required'}))
    arrival_latlng = forms.CharField(widget=forms.HiddenInput(), required=False,)
    arrival = forms.CharField(widget=forms.TextInput(attrs={'class': 'field',
                                                            'placeholder': 'Indiquez un lieu',
                                                            'autocomplete': 'on', 'required': 'required'}))
    previousDeparture = forms.CharField(widget=forms.HiddenInput(), required=False)
    previousArrival = forms.CharField(widget=forms.HiddenInput(), required=False)
    date = forms.CharField(widget=forms.TextInput(attrs={'required':'required', 'aria-invalid': 'true'}))
    dateGo = forms.CharField(widget=forms.HiddenInput(), required=False)
    dateBack = forms.CharField(widget=forms.HiddenInput(), required=False)
    timeGo = forms.CharField(widget=forms.HiddenInput(), required=False)
    timeBack = forms.CharField(widget=forms.HiddenInput(), required=False)
    timeMin = forms.CharField(widget=forms.TimeInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm', 'value': '07:00'}))
    timeMax = forms.CharField(widget=forms.TimeInput(attrs={'class': 'time', 'data-format': 'HH:mm',
                                                         'data-template': 'HH : mm', 'value': '08:00'}))


class ResearchFormDisplay(forms.ModelForm):
    selected = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'selected_field'}))
    providerDeparture = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}), required=False,)
    providerArrival = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}), required=False,)
    providerName = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'non-modifiable'}))
    providerIdUser = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
    detourboth = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    detour = forms.CharField(required=False, widget=forms.HiddenInput())
    detourkm = forms.CharField(required=False, widget=forms.HiddenInput())


    class Meta:
        model = Research
        fields = ['idCalendar', 'idPath', 'detour', 'streetDeparture', 'streetArrival', 'validated', 'available', 'detourkm', 'isGo']
        widgets = {
            'idCalendar': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'idPath': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetDeparture': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetArrival': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'validated': forms.HiddenInput(),
            'available': forms.HiddenInput(),
            'isGo': forms.HiddenInput(attrs={'readonly':'readonly'})
            }


class ResearchForm2(forms.ModelForm):
    providerPhone = forms.CharField(widget=forms.HiddenInput(), required=False)
    providerName = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False,)
    providerIdUser = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
    date = forms.DateField(widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
    
    class Meta:
        model = Research
        fields = ['idCalendar', 'idPath', 'detour', 'detourkm', 'streetDeparture', 'streetArrival', 'available', 'validated', 'isGo']
        widgets = {
            'idCalendar': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'idPath': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'detour': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'detourkm': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetDeparture': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetArrival': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'available': forms.HiddenInput(),
            'validated': forms.CheckboxInput(),
            'isGo': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            }
            
            
'''class HistoricForm(forms.ModelForm):

    class Meta:
        model = Historic
        fields = ['idCalendar', 'idPath', 'detour', 'detourkm', 'streetDeparture', 'streetArrival', 'validated', 'date']
        widgets = {
            'idCalendar': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'idPath': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'detour': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'detourkm': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetDeparture': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'streetArrival': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'validated': forms.CheckboxInput(),
            'date': forms.HiddenInput(attrs={'readonly':'readonly'}),
            }'''