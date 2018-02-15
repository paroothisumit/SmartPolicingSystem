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
function getPositionObject(lat,lng)
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
    console.log('New Marker');
    var pos=getPositionObject(lat,lng);
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
  positionToSiteObject[getPositionObject(lat,lng)]=siteObject;
  siteObject.addMarker();

}


function onClick(arg)
{
  console.log(arg.latLng.lat());
  console.log(positionToSiteObject[getPositionObject(arg.latLng.lat(),arg.latLng.lng())]);

}