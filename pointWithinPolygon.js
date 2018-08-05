const fs = require('fs')
const turf = require('turf')
const argv = require('minimist')(process.argv.slice(2))
const wards = require('./bbmp-wards.json')
const featureData = require('./' + argv['filename'])
const newProperty = argv['propertyName']

featureData.features.forEach(element => {
  wards.features.forEach(ward => {
    var isInside = turf.inside(element, ward)
    if (isInside) {
      if (ward.properties[newProperty]) {
        ward.properties[newProperty]++
      } else {
        ward.properties[newProperty] = 1
      }
    }
  })
})

fs.writeFile('wards-updated.json', JSON.stringify(wards), (err) => {
  if (err) throw err
  console.log('The file has been saved!')
})
