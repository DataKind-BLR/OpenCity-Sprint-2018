var map = L.map('map').setView([12.9889, 77.6221], 11)

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: ['a', 'b', 'c']
}).addTo(map)
$.getJSON("resources/data/bbmp-wards.json", function(data) {
    L.geoJson(data).addTo(map)
    
})
