window.onload=function(){document.getElementById("navbar").style.top=0;document.getElementById("map").style.opacity=1;document.getElementById("map").style.transform="scale(1)";document.getElementById("loading").style.opacity="0";addStuffs()};var favoritesEnabled=!1;function toggleFavorites(){favoritesEnabled=!favoritesEnabled;if(favoritesEnabled){document.getElementById("favoritesButton").className="btn btn-default glyphicon glyphicon-star";for(var i=0;i<50;i++)hideMarker(i);}else{document.getElementById("favoritesButton").className="btn btn-default glyphicon glyphicon-star-empty";for(var i=0;i<50;i++)showMarker(i);}}
function toggleCard(myCard){var transitionTime="0.5s";try{if(event.shiftKey==!0){transitionTime="2s"}else{transitionTime="0.5s"}}catch(err){}
var cardStyle=document.getElementById(myCard).style;cardStyle.transitionDuration=transitionTime;if(cardStyle.opacity==0){cardStyle.right="0px";cardStyle.opacity=1;cardStyle.pointerEvents="auto"}else{cardStyle.right="-200px";cardStyle.opacity=0;cardStyle.pointerEvents="none"}
var others=document.getElementsByClassName('card');for(var i=0;i<others.length;i++){if(others[i].id!=myCard){console.log(others[i]);var tmp=others[i].style;tmp.transitionDuration=transitionTime;tmp.right="-200px";tmp.opacity=0;tmp.pointerEvents="none"}}}
function openHouseCard(id){if(document.getElementById("houseCard").style.opacity==0)
toggleCard("houseCard");var xmlHttp=new XMLHttpRequest();xmlHttp.onreadystatechange=function(){if(xmlHttp.readyState==4&&xmlHttp.status==200){res=JSON.parse(xmlHttp.responseText);document.getElementById("hAddress").innerText=res.address;document.getElementById("hRent").innerText=("$"+res.rent+" per month")}}
xmlHttp.open("GET",("/id/"+id),!0);xmlHttp.send(null)}
var map;var markerIcon;var markerIconHidden;var markers=[];function initMap(){var tufts={lat:42.406534,lng:-71.120160};map=new google.maps.Map(document.getElementById('map'),{zoom:15,center:tufts,disableDefaultUI:!0,zoomControl:!0,styles:[{featureType:'administrative.locality',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'poi',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'poi',elementType:'geometry',stylers:[{color:'#c5c39a'}]},{featureType:'poi.park',elementType:'geometry',stylers:[{color:'#c5c39a'}]},{featureType:'poi.park',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'road',elementType:'geometry',stylers:[{color:'#ffffff'}]},{featureType:'road',elementType:'geometry.stroke',stylers:[{color:'#212a37'}]},{featureType:'road',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'road.highway',elementType:'geometry',stylers:[{color:'#dbb784'}]},{featureType:'road.highway',elementType:'geometry.stroke',stylers:[{color:'#bd9a69'}]},{featureType:'road.highway',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'transit',elementType:'geometry',stylers:[{color:'#bbbbbb'}]},{featureType:'transit.station',elementType:'labels.text.fill',stylers:[{color:'#000000'}]},{featureType:'water',elementType:'geometry',stylers:[{color:'#90bada'}]},{featureType:'water',elementType:'labels.text.fill',stylers:[{color:'#000000'}]}]});markerIcon={url:"static/images/marker.png",scaledSize:new google.maps.Size(48,48),origin:new google.maps.Point(0,0),anchor:new google.maps.Point(24,48)};markerIconHidden={url:"static/images/markerhidden.png",scaledSize:new google.maps.Size(4,4),origin:new google.maps.Point(0,0),anchor:new google.maps.Point(2,5)}}
function addMarker(lat,lon,id){var position={lat:lat,lng:lon}
var tmp=new google.maps.Marker({position:position,icon:markerIcon,map:map});tmp.addListener("click",function(){openHouseCard(id)});markers.push(tmp)}
function hideMarker(i){markers[i].setIcon(markerIconHidden)}
function showMarker(i){markers[i].setIcon(markerIcon)}
function deleteMarker(i){markers[i].setMap(null);markers.splice(i,1);console.log(markers)}

