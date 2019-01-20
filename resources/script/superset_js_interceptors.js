// data Interceptor
d => {
    console.log(d);
    var no_of_color_segments = 10;

    var min = 0;
    var max = 35;
    var colorArray = interpolateColors("rgb(247, 148, 89)", "rgb(94, 79, 162)", no_of_color_segments);
    colorArray.push([73, 72, 192, 255])
    var updated =  d.map(add_color);
    console.log(updated)
    return updated;

    function add_color(item) {
        var score = item.polygon.properties.count_fire_station + item.polygon.properties.count_fuel +
                    item.polygon.properties.count_hospital + item.polygon.properties.count_library +
                    item.polygon.properties.count_police + item.polygon.properties.count_school +
                    item.polygon.properties.count_townhall + item.polygon.properties.count_university ;
        return {
            polygon: item.polygon.geometry.coordinates,
            ward: ' ward name:' + item.polygon.properties.Ward_Name +' Index score:' + score,
            // fillColor: colors.hexToRGB(getColor(Math.random() * 35))
            fillColor: getColor(score)
        }
    }

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function getColor(val) {
        var segment = Math.floor(((val * no_of_color_segments) / (max - min)));
        return colorArray[segment];
    }




    // Returns a single rgb color interpolation between given rgb color
    // based on the factor given; via https://codepen.io/njmcode/pen/axoyD?editors=0010
    function interpolateColor(color1, color2, factor) {
        if (arguments.length < 3) {
            factor = 0.5;
        }
        var result = color1.slice();
        for (var i = 0; i < 3; i++) {
            result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
        }
        return result;
    }

    // Function to interpolate between two colors completely, returning an array
    function interpolateColors(color1, color2, steps) {
        var stepFactor = 1 / (steps - 1),
            interpolatedColorArray = [];

        color1 = color1.match(/\d+/g).map(Number);
        color2 = color2.match(/\d+/g).map(Number);

        for(var i = 0; i < steps; i++) {
            interpolatedColorArray.push(interpolateColor(color1, color2, stepFactor * i));
        }

        return interpolatedColorArray;
    }
}

// tooltip generator

d => {
    return d.object.ward;
}

