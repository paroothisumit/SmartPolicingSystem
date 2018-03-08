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
      map: map
    });
    map.setCenter(pos);
    outer_this.marker.addListener('click',onClick);
  }
}
function addSurveillanceSite(surveillanceSite_)
{
  var siteObject=new surveillanceSite(surveillanceSite_);

  siteIDtoSiteObject[siteObject.siteId]=siteObject;
  positionToSiteObject.set(positionString(siteObject.lat,siteObject.lng),siteObject);
  siteObject.addMarker();
  //console.log(positionToSiteObject.get(positionString(lat,lng)));
  
}
function alertHandler(message)
{
  console.log("Alert Handling javascript");
  var siteObject=siteIDtoSiteObject[message.SourceID];
  siteObject.contentString=getStyledString(siteObject,message);
  
  siteObject.marker.setAnimation(google.maps.Animation.BOUNCE);
}
var infoWindow = new google.maps.InfoWindow({
    content:''
});
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
  siteObject.contentString=undefined;

}
