/**
 * Created by IntelliJ IDEA.
 * User: ishai
 * Date: 29/06/2011
 * Time: 14:27:44
 * To change this template use File | Settings | File Templates.
 */

var map;
var geo;
//var gmap;
var radius_layer;
var MARK_RADIUS = 0.02;

var cord_google = new OpenLayers.Projection("EPSG:4326");
var cord_map = new OpenLayers.Projection("EPSG:900913");

var USE_GOOGLE = false;

var marker;

$(document).ready( function ()
{
    geo = new google.maps.Geocoder();
});

function createMarker(ll, popupContentHTML, closeBox, overflow) {
            popupClass=OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
            'autoSize': true,
            'backgroundColor':"red"
        });
            var feature = new OpenLayers.Feature(radius_layer, ll);
            feature.closeBox = closeBox;
            feature.popupClass = popupClass;
            feature.data.popupContentHTML = popupContentHTML;
            feature.data.overflow = (overflow) ? "auto" : "hidden";

            var marker = feature.createMarker();
             marker.icon.url = 'img/IGOL.png';
             marker.icon.size = (new OpenLayers.Size(16,16));
            var markerClick = function (evt) {
                if (this.popup == null) {
                    this.popup = this.createPopup(this.closeBox);
                    map.addPopup(this.popup);
                    this.popup.show();
                } else {
                    this.popup.toggle();
                }
                currentPopup = this.popup;
                OpenLayers.Event.stop(evt);
            };
            marker.events.register("mouseover", feature, markerClick);
            marker.events.register("mouseout", feature, markerClick);
           return  marker
        }

function addMarker(lng,lat,street,house,oldP,newP,apr,rooms){
         var lonlat = new OpenLayers.LonLat(lng,lat).transform(
	           cord_google,
	           cord_map
	       );
        if (apr==0){
            apr='לא צויין';
        }
        if (rooms==0){
            rooms=' לא צויין';
        }
        var text;
        text="כתובת:";
        text+=street+" "+house+"  דירה: "+apr+"<br>";
        text+="מספר חדרים:";
        text+=rooms+"<br>";
        text+=' שכ"ד עלה מ-';
        text+=oldP;
        text+=" ל-";
        text+=newP;
        text='<p style="text-align:right; font-size:11px; color:black;">'+text+'</p>';
        marker = createMarker(lonlat,text,false,false);
        radius_layer.addMarker(marker);
}

function redrawMarkers(){
    radius_layer.redraw();
}

function addMarkers(list,target){
    for (var i=0;i<list.length;i++){
        var lonlat = new OpenLayers.LonLat(list[i][0],list[i][1]).transform(
	           cord_google,
	           cord_map
	       );
        marker = new OpenLayers.Marker( lonlat );
        radius_layer.addMarker(marker);
    }
    radius_layer.redraw();
}

function init_map(target, center)
{
    if(!center)
        center = { lon : 34.8, lat :32.05 };
    var loc  = new OpenLayers.LonLat(center.lon,center.lat).transform(
	           cord_google,
	           cord_map
	       );
    if(!USE_GOOGLE)
    {

        map = new OpenLayers.Map({
            div: target,
            allOverlays: true
            //maxExtent : new OpenLayers.Bounds(-30, 36.095, -30, 43.095)
        });

        var osm = new OpenLayers.Layer.OSM();
//        gmap = new OpenLayers.Layer.Google("Google Streets", {visibility: false});
        radius_layer = new OpenLayers.Layer.Markers('radius_layer',{visibility: true} );

        // note that first layer must be visible
        map.addLayers([osm, radius_layer]);//, gmap]);
        map.setCenter(loc,13);
        //    map.addControl(new OpenLayers.Control.LayerSwitcher());
       //map.zoomToMaxExtent();
    }
}

function set_center()
{
    var location = get_location_from_map_center();
    geo.geocode( { latLng: location },function(results,status)
    {
        update_location_callback(location, null, results[0].formatted_address);
    });
}

function get_location_from_map_center()
{
    if( USE_GOOGLE)
    {
        return map.getCenter();
    }
    else
    {
        var ol = map.getCenter().transform( cord_map, cord_google );
        return new google.maps.LatLng(ol.lat, ol.lon);
    }
}

function get_location_from_address(address, region, success, error)
{
    if(!error)
        error = function(msg)
        {
            alert(msg);
        }
    if(!success)
        success = show_location_on_map;

    var params = { address : address};
    if(region)
        params['region'] = region;
    geo.geocode( params, function(results,status)
    {
        if( !results)
        {
            error('problem with Google API');
            return;
        }
        switch(results.length)
        {
            case 0:
                error('address not found');
                break;
            case 1:
                success(results[0].geometry.location, results[0].geometry.viewport, results[0].formatted_address);
                break;
            default:
                error('found multiple addresses');
                break;
        }
    });

}

function show_location_on_map(location, viewport,address)
{
    if( USE_GOOGLE)
    {
        map.setCenter(location);
        map.fitBounds(viewport);
        marker.setPosition = location;
    }
    else
    {
//        if(radius_layer)
//            map.removeLayer(radius_layer);
        var correspondingOLLonLat = new OpenLayers.LonLat(location.lng(),location.lat()).transform(
	           cord_google,
	           cord_map
	       );
        //var gLatLng = new google.maps.LatLng(location.lat(),location.lng());
        //var olLonLat = gmap.getOLLonLatFromMapObjectLonLat(gLatLng);
        marker = new OpenLayers.Marker( new OpenLayers.LonLat(0.0,0.0) );
        marker.lonlat = correspondingOLLonLat;
        radius_layer.clearMarkers();
        radius_layer.addMarker(marker);
        radius_layer.redraw();
        map.setCenter(correspondingOLLonLat,14);
//        var bounds = new OpenLayers.Bounds();
//        var size = OpenLayers.Size(20, 20);
//        bounds.extend(new OpenLayers.LonLat(location.Ja - MARK_RADIUS,location.Ka - MARK_RADIUS));
//        bounds.extend(new OpenLayers.LonLat(location.Ja + MARK_RADIUS,location.Ka + MARK_RADIUS));
//        radius_layer = new OpenLayers.Layer.Image(
//        {
//            name : 'radius_layer',
//            url:'',
//            extent: bounds,
//            size:size
//        });
//        map.addLayer(radius_layer);
    }

}
var c_address_sel, c_lat_input_sel, c_lon_input_sel;
var c_change_delegate;

function init_address_box(address_sel,button, lat_input_sel, lon_input_sel,change_delegate)
{
    c_address_sel = address_sel;
    c_lat_input_sel = lat_input_sel;
    c_lon_input_sel = lon_input_sel;
    c_change_delegate = change_delegate;
    $(button,main_content).click( function()
    {
        var address = $(c_address_sel,main_content).val();
        get_location_from_address(address,null,update_location_callback);
    });
}

function update_location_callback(location,viewport,address)
{
    if(address)
        $(c_address_sel).val(address);
    var home_lat = location.lat();
    var home_lon = location.lng();
    $(c_lon_input_sel,main_content).val(home_lon);
    $(c_lat_input_sel,main_content).val(home_lat);
    show_location_on_map(location,viewport,address);
    if( c_change_delegate)
        c_change_delegate(location,viewport,address);
}