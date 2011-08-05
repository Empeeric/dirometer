from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response
from backend.models import RentReport

@cache_page
def home(request):
    good = RentReport.objects.filter(price_up=False)
    bad = RentReport.objects.filter(price_up=True)

    good_list=[]
    bad_list=[]

    for r in good:
        if r.lat and r.lng:
            t=[r.lng,r.lat]
            good_list.append(t)
    for r in bad:
        if r.lat and r.lng:
            t=[r.lng,r.lat]
            bad_list.append(t)
    args={
        'GOOD_LIST':good_list,
        'BAD_LIST':bad_list
    }
    return render_to_response('home.html',args)