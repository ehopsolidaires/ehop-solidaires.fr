# -*- coding: utf-8 -*-

# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from models import *
from django.contrib.auth.models import User as django_User

from datetime import datetime
from django import forms
from django.contrib.gis.geos import Point

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'mail': forms.EmailInput(attrs={'aria-invalid': 'true', 'pattern': 'email', 'required': 'required'}),
        }
        exclude = ['name', 'firstname', 'sex', 'city', 'zipCode', 'phone', 'idHomeAddress', 'idWorkAddress']

        
class EmailAuthBackend(object):


    def authenticate(self,username=None, password=None):
        try:
            user = django_User.objects.get(email=username)
            if user and check_password(password, user.password):
                return user
        except django_User.DoesNotExist:
            return None
        
        
    def authenticate2(self,username=None, password=None):
        try:
            user = Provider.objects.filter(idUser__mail__contains=username).first()
            if user and (check_password(password, user.password)):
                return user
        except User.DoesNotExist:
            return None
            
    def auth_email(self, username=None):
        try:
            user = Provider.objects.filter(idUser__mail__contains=username).first()
            if user:
                return user
        except User.DoesNotExist:
            return None
            
    def auth_email2(self, username=None):
        try:
            user = django_User.objects.get(email=username)
            if user:
                return user
        except User.DoesNotExist:
            return None


class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'required': 'required'}))
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'required': 'required'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'maxlength': '10', 'aria-invalid': 'true', 'pattern': 'phone', 'required': 'required'}))
    sender = forms.EmailField(widget=forms.EmailInput(attrs={'aria-invalid': 'false', 'pattern': 'email'}), required=False)
    subjectCHOICES = (('Demandeur','Je cherche un trajet'),('Offreur','Je souhaite proposer un trajet'),
                      ('Infos','Informations diverses'),('Autre','Autre'))
    subject = forms.ChoiceField(choices=subjectCHOICES)
    goalOfApplicationCHOICES = [('', '')] + list(MenusSettings.objects.filter(type="goalOfApplication").values_list('string', 'string'))
    goalOfApplication = forms.ChoiceField(widget=forms.Select(attrs={'required':'required'}), choices=goalOfApplicationCHOICES, required=False)
    yearOfBirthCHOICES = (tuple((str(n), str(n)) for n in range(1900, datetime.now().year - 15))+(('',''),))[::-1]
    yearOfBirth = forms.ChoiceField(widget=forms.Select(attrs={'required':'required'}), choices=yearOfBirthCHOICES, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'required': 'required'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['goalOfApplication'].choices = get_menus_settings('goalOfApplication')


def get_menus_settings(type, required=True):
    if required:
        return [('', '')] + list(MenusSettings.objects.filter(type=type).values_list('string', 'string'))
    else:
        return list(MenusSettings.objects.filter(type=type).values_list('string', 'string'))


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={'required': 'required'}),
            'firstname': forms.TextInput(attrs={'required': 'required'}),
            'sex': forms.RadioSelect(attrs={'required': 'required'}),
            'city': forms.TextInput(attrs={'required': 'required'}),
            'zipCode': forms.TextInput(attrs={'maxlength': '5', 'aria-invalid': 'true', 'pattern': 'zipCode',
                                              'required': 'required'}),
            'mail': forms.EmailInput(attrs={'aria-invalid': 'true', 'pattern': 'email', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'maxlength': '10', 'aria-invalid': 'true',
                                            'pattern': 'phone', 'required': 'required'}),
        }
        exclude = ['idHomeAddress', 'idWorkAddress']


class ProviderRegisterForm(forms.ModelForm):
    class Meta:
        model = Provider
        howKnowledgeCHOICES = get_menus_settings('howKnowledge')
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'password', 'required': 'required'}),
            'company': forms.TextInput(attrs={'list':'datalistCompany', 'autocomplete':'off'}),
            'howKnowledge': forms.Select(attrs={'required':'required'}, choices=howKnowledgeCHOICES)
        }
        exclude = ['idUser', 'is_active', 'last_login']

    def __init__(self, *args, **kwargs):
        super(ProviderRegisterForm, self).__init__(*args, **kwargs)
        self.fields['howKnowledge'].choices = get_menus_settings('howKnowledge')


class ProviderForm2(forms.ModelForm):
    class Meta:
        model = Provider
        howKnowledgeCHOICES = [('','')] + list(MenusSettings.objects.filter(type="howKnowledge").values_list('string', 'string'))
        widgets = {
            'company': forms.TextInput(attrs={'list': 'datalistCompany', 'autocomplete': 'off'}),
            'howKnowledge': forms.Select(attrs={'required': 'required'}, choices=howKnowledgeCHOICES)
        }
        exclude = ['idUser', 'is_active', 'last_login', 'password']

    def __init__(self, *args, **kwargs):
        super(ProviderForm2, self).__init__(*args, **kwargs)
        self.fields['howKnowledge'].choices = get_menus_settings('howKnowledge')


class AddressRegisterForm(forms.ModelForm):
    latlng = forms.CharField(widget=forms.HiddenInput(), required=False,)
    cityHide = forms.CharField(widget=forms.HiddenInput(), required=False,)
    zipCodeHide = forms.CharField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = Address
        widgets = {
            'street':forms.TextInput(attrs={'class': 'field', 'placeholder': 'Indiquez un lieu',
                                            'autocomplete': 'on', 'required': 'required'}),
        }
        exclude = ['idAddress', 'point', 'city', 'zipCode']

    def clean(self):
        cleaned_data = super(AddressRegisterForm, self).clean()
        coord = cleaned_data['latlng'].replace('(', '')
        city = cleaned_data['cityHide']
        zipcode = cleaned_data['zipCodeHide']
        if city == "":
            city = "undefined"
        if zipcode == "undefined" or zipcode == "":
            zipcode = 0
        if coord == "" or coord == "undefined":
            raise forms.ValidationError("Bad address")
        coord = coord.replace(')', '')
        coordTab = coord.split(',')
        cleaned_data['point'] = 'POINT(%f %f)' % (float(coordTab[0]), float(coordTab[1]))
        cleaned_data['city'] = city
        cleaned_data['zipCode'] = zipcode
        return cleaned_data


class AddressRegisterFormWork(forms.ModelForm):
    latlng = forms.CharField(widget=forms.HiddenInput(), required=False,)
    cityHide = forms.CharField(widget=forms.HiddenInput(), required=False,)
    zipCodeHide = forms.CharField(widget=forms.HiddenInput(), required=False,)

    class Meta:
        model = Address
        widgets = {
            'street': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Indiquez un lieu', 'autocomplete': 'on',
                                            'required': 'required'}),
        }
        exclude = ['idAddress', 'point', 'city', 'zipCode']

    def clean(self):
        cleaned_data = super(AddressRegisterFormWork, self).clean()
        coord = cleaned_data['latlng'].replace('(', '')
        city = cleaned_data['cityHide']
        zipcode = cleaned_data['zipCodeHide']

        if city == "":
            city = "undefined"
        if zipcode == "undefined" or zipcode == "":
            zipcode = 0
        if coord == "" or coord == "undefined":
            raise forms.ValidationError("Bad address")
        coord = coord.replace(')', '')
        coordtab = coord.split(',')
        cleaned_data['point'] = 'POINT(%f %f)' % (float(coordtab[0]), float(coordtab[1]))
        cleaned_data['city'] = city
        cleaned_data['zipCode']= zipcode
        return cleaned_data


class PathDepartureRegisterForm(forms.ModelForm):
    class Meta:
        model = Path
        widgets = {
            'type': forms.HiddenInput(),
            'day': forms.HiddenInput(),
            'weekNumber': forms.HiddenInput(),
            'schedule': forms.TimeInput(attrs={'class': 'time', 'data-format': 'HH:mm', 'data-template': 'HH : mm',
                                               'value': '08:00'}),
        }
        exclude = ['idPath', 'idProvider', 'departure', 'arrival', 'startingWeek']


class PathArrivalRegisterForm(forms.ModelForm):
    class Meta:
        model = Path
        widgets = {
            'type': forms.HiddenInput(),
            'day': forms.HiddenInput(),
            'weekNumber': forms.HiddenInput(),
            'schedule': forms.TimeInput(attrs={'class': 'time', 'data-format': 'HH:mm', 'data-template': 'HH : mm',
                                               'value':'18:00'}),
        }
        exclude = ['idPath', 'idProvider', 'departure', 'arrival', 'startingWeek']

class TestUserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={'required': 'required'}),
            'firstname': forms.TextInput(attrs={'required': 'required'}),
            'city': forms.TextInput(attrs={'required': 'required'}),
            'zipCode': forms.TextInput(attrs={'maxlength': '5', 'aria-invalid': 'true', 'pattern': 'zipCode', 'required': 'required'}),
            'mail': forms.EmailInput(attrs={'aria-invalid': 'true', 'pattern': 'email', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'maxlength': '10', 'aria-invalid': 'true', 'pattern': 'phone', 'required': 'required'}),
        }
        exclude = ['idHomeAddress', 'idWorkAddress', 'sex']


class newMdpForm(forms.Form):
    oldmdp = forms.CharField(widget=forms.PasswordInput(), label='Ancien mot de passe', required=True)
    newmdp1 = forms.CharField(widget=forms.PasswordInput(), label='Nouveau mot de passe', required=True)