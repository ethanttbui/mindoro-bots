// Setting up Leaflet
var mymap = L.map('gismap').setView([13.1162, 121.0794], 10);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiZXRoYW5idWkiLCJhIjoiY2o4YjkzOTFwMHFhcjJ3cHVuZ3FqMmZqcCJ9.aEWaicVx_V-PvySMW3pf1Q'
}).addTo(mymap);


// Data
var coordByTime = {0 : [13.0, 121.0], 100 : [13.1, 121.1], 200 : [13.2, 121.2]}
var coords = [[13.0, 121.0], [13.1, 121.1], [13.2, 121.2]]

// Add pins and images
for (var key in coordByTime) {
  var marker = new L.marker(coordByTime[key]).bindPopup('<img class="image" src="images/' + key + '.jpg"/>').addTo(mymap);
}

// Draw path
var path = L.polyline(coords).addTo(mymap)
