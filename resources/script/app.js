var map = L.map('map').setView([12.9889, 77.6221], 11)

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: ['a', 'b', 'c']
}).addTo(map)
var data
$.getJSON('resources/data/bbmp-wards.json', function (data) {
  geojson = L.geoJson(data, {
    style: style,
    onEachFeature: onEachFeature
  }).addTo(map)

function style (feature) {
    return {
      weight: 2,
      opacity: 1,
      color: 'blue',
      dashArray: '3',
      fillOpacity: 0.1
    }
}

  L.geoJson(data, {style: style}).addTo(map)

function highlightFeature (e) {
    var layer = e.target

  layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
    })

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      layer.bringToFront()
  }
    info.update(layer.feature.properties)
}

  function resetHighlight (e) {
    geojson.resetStyle(e.target)
  info.update()
}

  function zoomToFeature (e) {
    map.fitBounds(e.target.getBounds())
}

  function onEachFeature (feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
    })
}

  geojson = L.geoJson(data, {
    style: style,
    onEachFeature: onEachFeature
  }).addTo(map)

var info = L.control()

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info') // create a div with a class "info"
    this.update()
    return this._div
};

  // method that we will use to update the control based on feature properties passed
  info.update = function (props) {
    this._div.innerHTML = '<h4>Bangalore BBMP wards</h4>' + (props
        ? '<b>' + props.Name + '</b><br />'
      : 'Hover over a ward')
};

  info.addTo(map)

})
