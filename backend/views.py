from django.http import HttpResponse
from models import RentReport
from google.appengine.api.urlfetch import Fetch
import settings
import logging
import urllib
try:
    import json
except ImportError:
    import simplejson as json

UNSPECIFIED=0

def getGeoLocation(city,street,number):
    '''g
        Convert given address to a set of coordinates
    '''

    params={
        'city':urllib.quote(city.encode('utf-8')),
        'street':urllib.quote(street.encode('utf-8')),
        'house':urllib.quote(number.encode('utf-8'))
    }

    url = settings.GEOCODE_URL %params
    res=Fetch(url)
    logging.info(res.content)
    coor=json.loads(res.content)['features'][0]['centroid']['coordinates']
    return coor[0],coor[1]
#    address=city+u','+street+u','+str(number)
#    gmaps = GoogleMaps(settings.GOOGLE_MAPS_API_KEY)
##    try:
#    lat, lng = gmaps.address_to_latlng(address)
#    return lat,lng
#    except :
#        logging.info("FAILED^^^^^^^")
#        return None,None


def addReport(request):

    i_city=request.POST.get('city')
    i_street=request.POST.get('street')
    i_address=request.POST.get('address')
    i_apartment=request.POST.get('apartment')
    i_oldPrice=request.POST.get('oldPrice')
    i_newPrice=request.POST.get('newPrice')
    i_rooms=request.POST.get('rooms')

    if not i_apartment:
        i_apartment=UNSPECIFIED
    if not i_rooms:
        i_rooms=UNSPECIFIED
    report, created=RentReport.objects.get_or_create(city=i_city,street=i_street,address=i_address,apartment=i_apartment)
    if created:
        report.old_price=int(i_oldPrice)
        report.new_price=int(i_newPrice)
        report.num_of_rooms=i_rooms
        lat,lng=getGeoLocation(i_city,i_street,i_address)
        if lat and lng:
            report.lat=lat
            report.lng=lng
        if i_oldPrice<i_newPrice:
            report.price_up=True
        else:
            report.price_up=False
        report.save()
    else:
        report.new_price=int(i_newPrice)
        if i_rooms!=UNSPECIFIED:
            report.num_of_rooms=i_rooms
    if request.POST.get('respHtml'):
        return HttpResponse('Html will come here')
    else:
        return HttpResponse('Ok')

def makeQuery(request):
    i_city=request.POST.get('city')
    i_street=request.POST.get('street')
    i_address=request.POST.get('address')
    i_apartment=request.POST.get('apartment')

    reports=RentReport.objects.filter(city=i_city,street=i_street,address=i_address)
    logging.info(reports)
    if len(reports)==0:
       return HttpResponse("");
    else:
        uc=False
        resp=""
        for report in reports:
            if report.apartment!=UNSPECIFIED:
                resp=resp+str(report.apartment)+" "
            else:
                uc=True
        if uc:
            resp=resp+" -1"
        return HttpResponse(resp)

def update_mobile(request):
    logging.info("POST:"+str(request.POST))
    return HttpResponse('ok')

def get_sync_data(request):
     return HttpResponse(json.dumps(settings.CHECK_LIST))