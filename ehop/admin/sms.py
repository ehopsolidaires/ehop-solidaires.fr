#  -*- coding: utf-8 -*-

# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3
from OvhApi import *
import OvhApi
from ehop.settings import APP_KEY, APP_SEC, CONS_KEY, SERVICE_NAME
import datetime
from ehopSolidaire_providers_register.models import SMS
from django.db.models import Q


def send(receiver, tag, message, noStop):
    if(receiver[1]!= '6' and receiver[1]!= '7'):
        return ValueError("Receiver must be a mobile phone number: "+receiver)
    api = Api(OvhApi.OVH_API_EU, APP_KEY, APP_SEC, CONS_KEY)
    content = {
        'tag': tag,
        'message': message,
        'noStopClause': noStop,
        'receivers': [format_phone_FR_to_inter(receiver)],
        'senderForResponse': True
    }
    r = api.post("/sms/"+SERVICE_NAME+"/jobs", content)
    SMS.objects.create(sender="EHOP", receiver=receiver, tag=tag, message=message, date=datetime.datetime.now(), read=True)
    print r
    r = 0
    return r


def get_sms_list(user_phone, read=True):
    SMS.objects.filter(Q(receiver=user_phone) | Q(sender=user_phone)).order_by('-date').update(read=read)
    return SMS.objects.filter(Q(receiver=user_phone) | Q(sender=user_phone)).order_by('-date')[:30][::-1]


def update(delete = True):
    api = Api(OvhApi.OVH_API_EU, APP_KEY, APP_SEC, CONS_KEY)
    r_ids = api.get("/sms/"+SERVICE_NAME+"/incoming")

    for id in r_ids:
        while True:
            r = api.get("/sms/"+SERVICE_NAME+"/incoming/"+str(id))
            print r
            if r['message'] != u'Internal call failed':
                break
        sender = format_phone_inter_to_FR(r['sender'])
        tag = r['tag']
        message = r['message']
        if "+02:00" in r['creationDatetime']:
            date = datetime.datetime.strptime((r['creationDatetime']).replace("T"," "),"%Y-%m-%d %H:%M:%S+02:00")
        elif "+01:00" in r['creationDatetime']:
            date = datetime.datetime.strptime((r['creationDatetime']).replace("T"," "),"%Y-%m-%d %H:%M:%S+01:00")
        SMS.objects.create(sender=sender, receiver="EHOP", tag=tag, message=message, date=date, read=False)
        if delete:
            api.delete("/sms/"+SERVICE_NAME+"/incoming/"+str(id))


def format_phone_FR_to_inter(phone):
    return '+33'+phone[1:]


def format_phone_inter_to_FR(phone):
    return phone.replace('+33','0')