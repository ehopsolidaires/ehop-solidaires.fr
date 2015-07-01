from ehopSolidaire_providers_register.models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ehop.settings import EMAIL_HOST_USER
from django.db.models import Q
import datetime


def update():
    now = datetime.datetime.now()
    date_min = monthdelta(now,-6)
    providers = Provider.objects.all().values_list('idUser', flat=True)
    us = User.objects.filter(Q(dateRegister__lt=date_min) & (Q(dateLastMailUpdate__lt=date_min) | Q(dateLastMailUpdate=None))).filter(idUser__in=providers).select_related('mail')
    for u in us:
        html_content = render_to_string('ehopSolidaire_providers_register/mail_update_inscription.html')
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives("Ehop-Solidaires - Confirmation d'inscription", text_content, EMAIL_HOST_USER, [u.mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    us.update(dateLastMailUpdate=now)


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)