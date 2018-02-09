var map;
intMap();
function intMap() {
  var uluru = {lat: -25.363, lng: 131.044};
  var home = {lat: 28.3670,  lng: 79.4304};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: home
  });
  var marker = new google.maps.Marker({
    position: uluru,
    map: map
  });
   var marker1 = new google.maps.Marker({
    position: home,
    map: map
  });
}
function addMarker(lati,longi){
  console.log('New Marker');
  var pos={lat:lati,lng:longi};
  var marker=new google.maps.Marker({
    position: pos,
    map: map
  });
  map.setCenter(pos);

}
