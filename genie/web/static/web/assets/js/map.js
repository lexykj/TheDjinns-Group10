let map;

//This init method is for the default map page with lesser functionality
function initDefault() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.743389, lng: -111.812058 },
    zoom: 16,
  });
}

function initMap() {
    event_id = document.getElementById("map").getAttribute("eventid");
    //The below code is for the defaultMap view

    url = "http://127.0.0.1:8000/api/map_data/?event_id="+event_id;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            addMap(data)
            
            for (let id in data['lots']) {
                addLot(data['lots'][id])
            }
        });
}

function initLot() {
    lot_id = document.getElementById("map").getAttribute("lotid");
    //The below code is for the lot specific view

    url = "http://127.0.0.1:8000/api/lot_data/?lot_id="+lot_id;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            addLotMap(data)
        });
}

function addMap(data) {
    const Event = { lat: data['latitude'], lng: data['longitude'] };

    map = new google.maps.Map(document.getElementById("map"), {
        center:     Event,
        zoom:       15,
        mapId:      'da9b4daab158add3',
    });

    const eventMarker = new google.maps.Marker({
        position:   Event,
        map:        map,
    });

    const eventString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">' + data['name'] +'</h1>' +
        '<div id="bodyContent">' +
        "<p>" + data['description'] +"</p>" +
        "<p>" + data['date'] +"</p>" +
        "<p>" + data['address'] +"</p>" +
        "</div>" +
        "</div>";

    const eventWindow = new google.maps.InfoWindow({
        content: eventString,
    });

    eventMarker.addListener("click", () => {
        map.setCenter(eventMarker.getPosition());
        eventWindow.open(map, eventMarker);
    });
}

function addLot(data) {
    const Lot = { lat: data['latitude'], lng: data['longitude'] };

    const lotMarker = new google.maps.Marker({
        position:   Lot,
        icon:       'https://maps.google.com/mapfiles/kml/shapes/parking_lot_maps.png',
        map:        map,
    });

    const lotString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">' + data['name'] +'</h1>' +
        '<div id="bodyContent">' +
        "<p>" + data['address'] +"</p>" +
        "</div>" +
        "</div>";

    const lotWindow = new google.maps.InfoWindow({
        content:    lotString,
    });

    lotMarker.addListener("click", () => {
        map.setCenter(lotMarker.getPosition());
        lotWindow.open(map,lotMarker);
    });
}

function addLotMap(data) {
    const Lot = { lat: data['latitude'], lng: data['longitude'] };

    map = new google.maps.Map(document.getElementById("map"), {
        center:     Lot,
        zoom:       15,
        mapId:      'da9b4daab158add3',
    });

    const lotMarker = new google.maps.Marker({
        position:   Lot,
        map:        map,
    });

    const lotString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">' + data['name'] +'</h1>' +
        '<div id="bodyContent">' +
        "<p>" + data['address'] +"</p>" +
        "</div>" +
        "</div>";

    const lotWindow = new google.maps.InfoWindow({
        content: lotString,
    });

    lotMarker.addListener("click", () => {
        map.setCenter(lotMarker.getPosition());
        lotWindow.open(map,lotMarker);
    });
}