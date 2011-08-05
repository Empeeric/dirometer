from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from models import RentReport
from google.appengine.api.urlfetch import Fetch
import settings
from googlemaps import GoogleMaps
import logging
import urllib
try:
    import json
except ImportError:
    import simplejson as json

UNSPECIFIED_APARTMENT=-1

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

    if not i_apartment:
        i_apartment=UNSPECIFIED_APARTMENT
    report, created=RentReport.objects.get_or_create(city=i_city,street=i_street,address=i_address,apartment=i_apartment)
    if created:
        report.old_price=int(i_oldPrice)
        report.new_price=int(i_newPrice)
        lat,lng=getGeoLocation(i_city,i_street,i_address)
        if lat and lng:
            logging.info("&&&&&^^^^^^^&&&&&")
            report.lat=lat
            report.lng=lng
        if i_oldPrice<i_newPrice:
            report.price_up=True
        else:
            report.price_up=False
        report.save()
    else:
        pass
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
       logging.info("########TTTTTTTT")
       return HttpResponse("");
    else:
        uc=False
        resp=""
        for report in reports:
            if report.apartment!=UNSPECIFIED_APARTMENT:
                resp=resp+str(report.apartment)+" "
            else:
                uc=True
        if uc:
            resp=resp+"@"
        logging.info("########"+resp)
        return HttpResponse(resp)