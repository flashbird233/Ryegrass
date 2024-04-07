let map;

function initMap() {

    var ausBounds = {
        north: -9,
        south: -45,
        east: 155,
        west: 111
    }

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: {lat: -37.813611, lng: 144.963056},
        streetViewControl: false,
        minZoom: 4,
        disableDefaultUI: true,
        fullscreenControl: true,
        restriction: {
            latLngBounds: ausBounds,
            strictBounds: true
        }
    });

    locations.forEach(function (location) {
        new google.maps.Marker({
            position: {
                lat: location.lat,
                lng: location.lng
            },
            map: map,
            title: location.rye_vernacular_name,
            icon: {
                url: "/static/images/map_icon.png",
                scaledSize: new google.maps.Size(30, 30)
            },
        });
    });
    
}

window.initmap = initMap;