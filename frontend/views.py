from django.shortcuts import render_to_response,redirect
from backend.models import RentReport
import settings

def getMapArgs():
    good=[] #list(RentReport.objects.filter(price_up=False))
    bad= list(RentReport.objects.filter(price_up=True))

    good_list=[]
    bad_list=[]

    for r in good:
        if r.lat and r.lng:
            good_list.append(r)
    for r in bad:
        if r.lat and r.lng:
            bad_list.append(r)
    bad_list=sorted(bad_list,key=lambda report: report.new_price-report.old_price,reverse=True)
    bad_list=bad_list[:settings.MAX_MARKERS]
    args={
        'GOOD_LIST':good_list,
        'BAD_LIST':bad_list
    }
    return args

def home(request):
    return render_to_response('home.html',getMapArgs())

def widget(request):
    return render_to_response('widget.html',getMapArgs())
