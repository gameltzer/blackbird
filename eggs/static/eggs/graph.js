var thisContainer = document.querySelector('.chart-container');

// This lets us access our json File. 
var requestURL = 'static/eggs/resultJson.json';
var request = new XMLHttpRequest();
request.open('GET',requestURL);
request.responseType = 'json';
request.send();


request.onload = function() {
    var results = request.response;
    makeChart(results);
};

// # this is just a test
function makeChart(jsonObj){
    var jsonGroup = [];
    var jsonData = [];
    for(var i = 0; i < jsonObj.length; i++){
        jsonGroup[i] = jsonObj[i].fields.batch;
        jsonData[i] = jsonObj[i].fields.significantVariantCount;
    }

    canvas = makeCanvas(); 
    var myChart = new Chart(canvas,{
        type: 'bar',
        data: {
            labels: jsonGroup,
            datasets: [{
                label: '# of mutations',
                data: jsonData,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    barThickness: 50   
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
    console.log(myChart.options);
}

function makeCanvas(){
    var myCanvas = document.createElement('canvas');
    thisContainer.appendChild(myCanvas);
    return myCanvas;
}