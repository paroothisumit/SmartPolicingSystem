var map;
intMap();
var siteIDtoSiteObject=new Map();
var positionToSiteObject=new Map();
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
function surveillanceSite(siteId,lat,lng)
{
  this.siteId=siteId,
  this.lat=lat,
  this.lng=lng;
  this.marker=undefined;
  var outer_this=this;
  
  this.addMarker=function()
  {
    
    var pos=positionObject(lat,lng);
    outer_this.marker=new google.maps.Marker({
      position: pos,
      map: map
    });
    map.setCenter(pos);
    outer_this.marker.addListener('click',onClick);
  }
}
function addSurveillanceSite(siteId,lat,lng)
{
  var siteObject=new surveillanceSite(siteId,lat,lng);

  siteIDtoSiteObject[siteId]=siteObject;
  positionToSiteObject.set(positionString(lat,lng),siteObject);
  siteObject.addMarker();
  console.log(positionToSiteObject.get(positionString(lat,lng)));
  
}
function alertHandler(siteId)
{
  console.log("Alert Handling javascript");
  var siteObject=siteIDtoSiteObject[siteId];
  siteObject.marker.setAnimation(google.maps.Animation.BOUNCE);
}
var infoWindow = new google.maps.InfoWindow({
    content:''
  });
function onClick(arg)
{

  //console.log(positionString(arg.latLng.lat(),arg.latLng.lng()))
  var siteObject=positionToSiteObject.get(positionString(arg.latLng.lat(),arg.latLng.lng()));
  
  var contentString=(siteObject.siteId.toString());
  infoWindow.setContent(contentString);
  console.log('Info Window Created');
  infoWindow.open(map,siteObject.marker);

}
