function setFileName(event) {
    event.srcElement.nextSibling.nextSibling.innerText = event.srcElement.files[0].name
}

function toggleContent(element) {
    if (element.style.maxHeight) {
        element.style.maxHeight = null;
    } else {
        element.style.maxHeight = element.scrollHeight + "px";
    }
}

function getCoordinates(lng, lat) {
    if (isNaN(lng) || isNaN(lat) || !lng || !lat) {
        return [33.074918, 68.970663];
    } else {
        return [parseFloat(lng), parseFloat(lat)];
    }
}
function createMap(mapContainer, lngContainer, latContainer) {
    lng = lngContainer.value
    lat = latContainer.value
    function setFormValues(lng, lat) {
        lngContainer.value = lng
        latContainer.value = lat
    }
    mapboxgl.accessToken = 'pk.eyJ1IjoiZm94eWxpbmUiLCJhIjoiY2xoNHg1YW01MDBqdzNjbXhjNXhqbWtmbyJ9.8hqV2_RfcMDY2Ax7mWPi1A';

    const map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/foxyline/clh4ycdv600on01qu29sk3s84',
        center: getCoordinates(lng, lat),
        zoom: 13,
    });

    const geo = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
    })
    const marker = new mapboxgl.Marker({
        draggable: true
    })
    if (!isNaN(lng) && !isNaN(lat)) {
        marker.setLngLat([lng, lat])
            .addTo(map);
    }

    geo.on('result', e => {
        geo.clear()
        marker.setLngLat(e.result.center)
            .addTo(map);
        setFormValues(e.result.center[0], e.result.center[1])

    });

    map.addControl(
        geo
    )
    function onDragEnd() {
        const lngLat = marker.getLngLat();
        setFormValues(lngLat.lng, lngLat.lat)
    }

    marker.on('dragend', onDragEnd);
}

function toggleMap(event) {
    event.srcElement.parentElement.nextSibling.nextSibling.children[0].innerHTML = ""
    toggleContent(event.srcElement.parentElement.nextSibling.nextSibling)
    lnt = event.srcElement.parentElement.parentElement.nextElementSibling.nextElementSibling.children[1]
    lat = event.srcElement.parentElement.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.children[1]
    createMap(event.srcElement.parentElement.nextSibling.nextSibling.children[0], lnt, lat)
}
