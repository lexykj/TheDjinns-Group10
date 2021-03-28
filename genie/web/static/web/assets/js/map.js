let map;

function initMap() {
    event_id = document.getElementById("map").getAttribute("eventid");
    url = "http://127.0.0.1:8000/api/map_data/?event_id="+event_id;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            makeEvent(data['latitude'], data['longitude']);
        });
}

function makeEvent(lat, lon) {
    const Event = { lat: lat, lng: lon };

    map = new google.maps.Map(document.getElementById("map"), {
        center:     Event,
        zoom:       15,
    });

    const eventMarker = new google.maps.Marker({
        position:   Event,
        map:        map,
    });

    const eventString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">Maverik Stadium</h1>' +
        '<div id="bodyContent">' +
        "<p>Make an API in Django to manage some of this?</p>" +
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