let map;

function initMap() {
    const Maverik = { lat: 41.752074, lng: -111.812874 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: Maverik,
        zoom: 15,
    });

    const marker = new google.maps.Marker({
        position: Maverik,
        map: map,
    });    
}