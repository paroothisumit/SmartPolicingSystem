var centroidX=0.0,centroidY=0.0;
var map;
intMap();
var sitesCollection=[];
var siteIDtoSiteObject=new Map();
var positionToSiteObject=new Map();
var safeIcon='markerImages/green-dot.png';
var alertIcon='markerImages/red-dot.png';
var infoWindow = new google.maps.InfoWindow({
  content:''
});

function intMap() 
{
  var origin={lat:25,lng:75};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: origin
  });

}

function positionString(lat,lng)
{
  
  return (lat.toFixed(8)).toString()+(lng.toFixed(8)).toString();
   
}

function positionObject(lat,lng)
{
  return {
    lat:lat,
    lng:lng
  };
}

function surveillanceSite(siteInfo)
{
  this.siteId=siteInfo.id,
  this.lat=siteInfo.latitude,
  this.lng=siteInfo.longitude;
  this.contentString=undefined;
  this.marker=undefined;
  this.description=siteInfo.description;
  this.contact=siteInfo.contact;
  this.address=siteInfo.address;
  var outer_this=this;
  
  this.addMarker=function()
  {
    
    var pos=positionObject(siteInfo.latitude,siteInfo.longitude);
    outer_this.marker=new google.maps.Marker({
      position: pos,
      map: map,
      icon: safeIcon
    });
    map.setCenter(pos);
    outer_this.marker.addListener('click',onClick);
    
  }
}
surveillanceSite.count=0;

function addSurveillanceSite(surveillanceSite_)
{
  var siteObject=new surveillanceSite(surveillanceSite_);
  sitesCollection.push(siteObject);
  centroidX+=siteObject.lat;
  centroidY+=siteObject.lng;
  siteIDtoSiteObject[siteObject.siteId]=siteObject;
  positionToSiteObject.set(positionString(siteObject.lat,siteObject.lng),siteObject);
  siteObject.addMarker();
  surveillanceSite.count++;
  readjustMap();
  //console.log(positionToSiteObject.get(positionString(lat,lng)));
}

function readjustMap()
{
  map.setCenter(positionObject(centroidX/surveillanceSite.count,centroidY/surveillanceSite.count));
  map.setZoom(getMaxZoom());
}

function getMaxZoom()
{
  var isZoomValid = function(zoom)
  {

    map.setZoom((zoom));
    for(var i=0;i<sitesCollection.length;i++)
    {
      
      if(!map.getBounds().contains(sitesCollection[i].marker.getPosition()))
      {
        return false;
      }
    }
    return true;
  }

  var beg = 3,end = 20;
  var itr=0;
  while(itr<6)
  {
    var mid=Math.floor((end+beg)/2);
    
    if(isZoomValid(mid))
    {
      beg=mid;
    }
    else
      end=mid;
    itr++;
  }
  return beg; 
  
}


function alertHandler(message)
{
  console.log("Alert Handling javascript");
  var siteObject=siteIDtoSiteObject[message.SourceID];
  siteObject.contentString=getStyledString(siteObject,message);
  map.panTo(positionObject(siteObject.lat,siteObject.lng));
  map.setZoom(15);
  siteObject.marker.setAnimation(google.maps.Animation.BOUNCE);
  siteObject.marker.setIcon(alertIcon);
}


infoWindow.addListener('closeclick',onInfoWindowClosed);
function onInfoWindowClosed()
{
  readjustMap();
}
function onClick(arg)
{

  //console.log(positionString(arg.latLng.lat(),arg.latLng.lng()))
  var siteObject=positionToSiteObject.get(positionString(arg.latLng.lat(),arg.latLng.lng()));
  if(siteObject.contentString == undefined)
    siteObject.contentString=getStyledString(siteObject);
  infoWindow.setContent(siteObject.contentString);
  console.log('Info Window Created');
  infoWindow.open(map,siteObject.marker);
  siteObject.marker.setAnimation(null);
  siteObject.marker.setIcon(safeIcon);
  siteObject.contentString=undefined;
  

}
