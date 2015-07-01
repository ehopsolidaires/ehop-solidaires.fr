# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from ehopSolidaire_providers_register.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ehop.settings import EMAIL_HOST_USER
from django.db.models import Q
import datetime


class Command(BaseCommand):
    help = 'Sends mail to 6 months old accounts'

    def handle(self, *args, **options):
        from ehopSolidaire_providers_register.update_mail import update
        update()


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)