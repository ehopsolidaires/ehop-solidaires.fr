# -*- coding: utf-8 -*-

# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.contrib.auth.models import check_password
from django import forms
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime, timedelta
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.
class Address(models.Model):
    idAddress = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=5)
    point = models.PointField(srid=4326) #spatial reference
    objects = models.GeoManager() #every GIS-based django model needs one of these for geospatial queries

    class Meta:
        verbose_name = 'Adresse'

    def __unicode__(self):
        return self.street

    def get_cleaned_street(self):
        return self.street.replace(", France","")


class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=255, null=True, unique=True, blank=True, verbose_name="Email")
    name = models.CharField(max_length=30, verbose_name="Nom")
    firstname = models.CharField(max_length=30, verbose_name="Prenom")
    city = models.CharField(max_length=255, verbose_name="Ville")
    zipCode = models.CharField(max_length=5, verbose_name="Code postal")
    phone = models.CharField(max_length=10, verbose_name="Numero de telephone")
    SEX_CHOICES = (
        ('H', 'M'),
        ('F', 'Mme'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=None, verbose_name="Sex")
    idHomeAddress = models.ForeignKey(Address, related_name="idHomeAddress", verbose_name="Adresse de domicile")
    idWorkAddress = models.ForeignKey(Address, related_name="idWorkAddress", verbose_name="Adresse de travail")
    dateRegister = models.DateTimeField(auto_now_add=True)
    dateLastConnection = models.DateTimeField(auto_now=True)
    dateLastCarSharing = models.DateTimeField(blank=True, null=True)
    dateLastMailUpdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Utilisateur'

    def get_address_home_link(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:ehopSolidaire_providers_register_address_change',
                                                             args=(self.idHomeAddress.idAddress,), ),
                                        (self.idHomeAddress))
        get_address_home_link.allow_tags = True
        get_address_home_link.short_description = 'Adresse de domicile'

    def get_address_work_link(self):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:ehopSolidaire_providers_register_address_change',
                                                             args=(self.idWorkAddress.idAddress,), ),
                                        (self.idWorkAddress))
        get_address_work_link.allow_tags = True
        get_address_work_link.short_description = 'Adresse de travail'

    def get_mail(self):
        if self.mail:
            return self.mail
        return ""


class Applicant(models.Model):
    idApplicant = models.AutoField(primary_key=True)
    carringAgency = models.CharField(max_length=50, blank=True, null=True)
    accompName = models.CharField(max_length=100, blank=True, null=True)
    accompFirstname = models.CharField(max_length=100, blank=True, null=True)
    accompPhone = models.CharField(max_length=20, blank=True, null=True)
    accompMail = models.CharField(max_length=200, blank=True, null=True)
    goalOfApplication = models.CharField(max_length=150, blank=True, null=True)
    yearOfBirth = models.CharField(max_length=4)
    identNum = models.CharField(max_length=20, unique=True, null=True, blank=True)
    scheduleType = models.CharField(max_length=100, null=True, blank=True)
    idUser = models.ForeignKey(User)


    def get_goalOfApplication(self):
        if self.goalOfApplication:
            return self.goalOfApplication
        return ""

    def get_carringAgency(self):
        if self.carringAgency:
            return self.carringAgency
        return ""

    class Meta:
        verbose_name = 'Demandeur'


class Provider(models.Model):
    idProvider = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    company = models.CharField(max_length=255, null=True, blank=True)
    howKnowledge = models.CharField(max_length=255)
    idUser = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Offreur'


class Path(models.Model):
    idPath = models.AutoField(primary_key=True)
    schedule = models.TimeField()
    schedule2 = models.TimeField(blank=True, null=True)
    type = models.IntegerField(max_length=1)
    weekNumber = models.CharField(max_length=1)
    day = models.CharField(max_length=10)
    idProvider = models.ForeignKey(Provider)
    startingWeek = models.IntegerField(max_length=10)
    departure = models.ForeignKey(Address, related_name="departure")
    arrival = models.ForeignKey(Address, related_name="arrival")

    def getPlanningType(self):
        if self.type == 0:
            return 'fixe'
        elif self.type == 1:
            return '2*8'
        elif self.type == 2:
            return '3*8'

    class Meta:
        verbose_name = 'Trajet'


class Calendar(models.Model):
    idCalendar = models.AutoField(primary_key=True)
    idApplicant = models.ForeignKey(Applicant)
    dateBeginningGo = models.DateField(max_length=20)
    scheduleBeginningGo = models.CharField(max_length=20)
    dateBeginningBack = models.DateField(max_length=20)
    scheduleBeginningBack = models.CharField(max_length=20)
    go = models.CharField(max_length=255)
    back = models.CharField(max_length=255)
    streetHome = models.CharField(max_length=255)
    streetWork = models.CharField(max_length=255)
    possibleMeetingSpot = models.CharField(max_length=150, blank=True, null=True)
    transportIssue = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(max_length=1024, null=True, blank=True)

    '''
        Returns the number of days selected in a calendar
    '''
    def get_numberof_selected_days(self):
        nb_go = 0
        nb_back = 0
        for go in self.go.split(','):
            if go == "R" or go == "V":
                nb_go += 1
        for back in self.back.split(','):
            if back == "R" or back == "V":
                nb_back += 1
        if nb_go > nb_back:
            return nb_go
        else:
            return nb_back

    '''
        Returns the number of days between first and last day selected
    '''
    def get_interval_days(self):
        l_go = [15,-1]
        l_back = [15,-1]
        for counter, go in enumerate(self.go.split(',')):
            if go == "R" or go == "V":
                if l_go[0] > counter:
                    l_go[0] = counter
                if l_go[1] < counter:
                    l_go[1] = counter
        for counter, back in enumerate(self.back.split(',')):
            if back == "R" or back == "V":
                if l_back[0] > counter:
                    l_back[0] = counter
                if l_back[1] < counter:
                    l_back[1] = counter
        interval_go = l_go[1] - l_go[0] + 1
        interval_back = l_back[1] - l_back[0] + 1
        if interval_go > interval_back:
            return interval_go
        else:
            return interval_back

    '''
        Returns the beginning date
    '''
    def get_beginning_date(self):
        if self.dateBeginningGo < self.dateBeginningBack:
            return self.dateBeginningGo
        else:
            return self.dateBeginningBack

    '''
        Returns a formatted streetHome-streetWork string
    '''
    def get_path(self):
        has_go = False
        for e in self.go.split(','):
            if e == "R" or e == "V":
                has_go = True
        split_streetHome = self.streetHome.split(',')
        split_streetWork = self.streetWork.split(',')

        # format streetHome if possible
        if split_streetHome.__len__() > 2:
            streetHome = split_streetHome[1]
        elif split_streetHome.__len__() == 2:
            streetHome = split_streetHome[0]
        else:
            streetHome = self.streetHome
        # format streetWork if possible
        if split_streetWork.__len__() > 2:
            streetWork = split_streetWork[1]
        elif split_streetWork.__len__() == 2:
            streetWork = split_streetWork[0]
        else:
            streetWork = self.streetWork

        if has_go:
            return streetHome+'-'+streetWork
        else:
            return streetWork+'-'+streetHome


class LinkCalendar(models.Model):
    idCalendar = models.ForeignKey(Calendar)
    idApplicant = models.ForeignKey(Applicant)

    class Meta:
        unique_together = ('idCalendar','idApplicant',)


class HistoricCalendar(models.Model):
    idHistoricCalendar = models.AutoField(primary_key=True)
    pourcentage = models.FloatField()
    idApplicant = models.ForeignKey(Applicant)
    dateBeginning = models.DateField(max_length=20)
    scheduleBeginningGo = models.CharField(max_length=20)
    scheduleBeginningBack = models.CharField(max_length=20)
    go = models.CharField(max_length=255)
    back = models.CharField(max_length=255)
    streetHome = models.CharField(max_length=255)
    streetWork = models.CharField(max_length=255)
    possibleMeetingSpot = models.CharField(max_length=150, blank=True, null=True)
    transportIssue = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(max_length=1024, null=True, blank=True)

    def get_transportIssue(self):
        if self.transportIssue:
            return self.transportIssue
        return ""

    '''
        Returns comment field or an empty string
    '''
    def get_comment(self):
        if self.comment:
            return self.comment
        return ""

    '''
        Returns the number of days selected in a calendar
    '''
    def get_numberof_selected_days(self):
        nb_go = 0
        nb_back = 0
        for go in self.go.split(','):
            if go == "R" or go == "V":
                nb_go += 1
        for back in self.back.split(','):
            if back == "R" or back == "V":
                nb_back += 1
        if nb_go > nb_back:
            return nb_go
        else:
            return nb_back

    '''
        Returns the number of days between first and last day selected
    '''
    def get_interval_days(self):
        l_go = [15,-1]
        l_back = [15,-1]
        for counter, go in enumerate(self.go.split(',')):
            if go == "R" or go == "V":
                if l_go[0] > counter:
                    l_go[0] = counter
                if l_go[1] < counter:
                    l_go[1] = counter
        for counter, back in enumerate(self.back.split(',')):
            if back == "R" or back == "V":
                if l_back[0] > counter:
                    l_back[0] = counter
                if l_back[1] < counter:
                    l_back[1] = counter
        interval_go = l_go[1] - l_go[0] + 1
        interval_back = l_back[1] - l_back[0] + 1
        if interval_go > interval_back:
            return interval_go
        else:
            return interval_back

    def get_last_week_number(self):
        date = self.dateBeginning + timedelta(days=self.get_interval_days())
        return int(date.strftime("%U"))

    def get_first_week_number(self):
        date = self.dateBeginning
        return int(date.strftime("%U"))


class Historic(models.Model):
    idHistoric = models.AutoField(primary_key=True)
    idHistoricCalendar = models.ForeignKey(HistoricCalendar)
    idPath = models.ForeignKey(Path)
    detour = models.CharField(max_length=20)
    detourkm = models.CharField(max_length=20)
    streetDeparture = models.CharField(max_length=255)
    streetArrival = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    date = models.DateField(max_length=20)


class Research(models.Model):
    idResearch = models.AutoField(primary_key=True)
    idCalendar = models.ForeignKey(Calendar)
    idPath = models.ForeignKey(Path)
    detour = models.CharField(max_length=20)
    detourkm = models.CharField(max_length=20)
    streetDeparture = models.CharField(max_length=255)
    streetArrival = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    isGo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Recherche'

    def archive(self, date, idHistoricCalendar):
        print date
        if self.validated:
            print "archive"
            Historic.objects.create(idHistoricCalendar=idHistoricCalendar, idPath=self.idPath, detour=self.detour,
                                               detourkm=self.detourkm, streetDeparture=self.streetDeparture,
                                               streetArrival=self.streetArrival, validated=True, date=date)


class Companies(models.Model):
    name = models.CharField(max_length=255)


class SMS(models.Model):
    sender = models.CharField(db_index=True, max_length=20)
    receiver = models.CharField(db_index=True, max_length=20)
    message = models.TextField()
    date = models.DateTimeField()
    tag = models.CharField(max_length=255)
    read = models.BooleanField(db_index=True, default=False)


class Intercommunity(models.Model):
    insee = models.CharField(max_length=5)
    zipCode = models.CharField(max_length=5)
    town = models.CharField(max_length=255)
    intercommunity = models.CharField(max_length=255)


class Deletion(models.Model):
    dateRegister = models.DateField()
    dateDelete = models.DateField()
    type = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    homeIntercommunity = models.CharField(max_length=255)
    workIntercommunity = models.CharField(max_length=255)

    def get_type_FR(self):
        if self.type == "provider":
            return "offreur"
        if self.type == "applicant":
            return "demandeur"