from django.shortcuts import render_to_response,redirect
from backend.models import RentReport
def home(request):
    good=RentReport.objects.filter(price_up=False)
    bad=RentReport.objects.filter(price_up=True)

    good_list=[]
    bad_list=[]

    for r in good:
        if r.lat and r.lng:
            good_list.append(r)
    for r in bad:
        if r.lat and r.lng:
            bad_list.append(r)
    args={
        'GOOD_LIST':good_list,
        'BAD_LIST':bad_list
    }
    return render_to_response('home.html',args)

import logging

def showAll(request):
    l=RentReport.objects.all()
    logging.info('#######'+str(len(l)))
    args={
        'LIST':l,
    }
    return render_to_response('showAll.html',args)