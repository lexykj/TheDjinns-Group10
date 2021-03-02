let map;    

function initMap() {
    const Maverik = { lat: 41.752074, lng: -111.812874 };
    const Lot     = { lat: 41.762074, lng: -111.812874 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: Maverik,
        zoom: 15,
    });

    const maverikMarker = new google.maps.Marker({
        position: Maverik,
        map: map,
    });

    const maverikString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">Maverik Stadium</h1>' +
        '<div id="bodyContent">' +
        "<p>Figure out a way for django to handel this</p>" +
        "</div>" +
        "</div>";
    
    const maverikWindow = new google.maps.InfoWindow({
        content: maverikString,
    });

    maverikMarker.addListener("click", () => {
        map.setCenter(maverikMarker.getPosition());
        maverikWindow.open(map, maverikMarker);
    });

    const lotMarker = new google.maps.Marker({
        position:   Lot,
        icon:       'https://maps.google.com/mapfiles/kml/shapes/parking_lot_maps.png',
        map:        map,
    });

    const lotString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">Example Parking Lot</h1>' +
        '<div id="bodyContent">' +
        "<p>Figure out a way for django to handel this</p>" +
        "</div>" +
        "</div>";

    const lotWindow = new google.maps.InfoWindow({
        content: lotString,
    });

    lotMarker.addListener("click", () => {
        map.setCenter(lotMarker.getPosition());
    });
}