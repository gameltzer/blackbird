var thisContainer = document.querySelector('.chart-container');

// This lets us access our json File. 
var requestURL = 'http://localhost:8000/static/eggs/resultJson.json';
var request = new XMLHttpRequest();
request.open('GET',requestURL);
request.responseType = 'json';
request.send();


request.onload = function() {
    var results = request.response;
    makeChart(results);
}

// # this is just a test
function makeChart(jsonObj){

    canvas = makeCanvas(); 
    var myChart = new Chart(canvas,{
        type: 'bar',
        data: {
            labels: [jsonObj[0].fields.batch],
            datasets: [{
                label: '# of mutations',
                data: [jsonObj[0].fields.significantVariantCount],
                backgroundColor: ['rgba(54, 162, 235, 0.2)'],
                borderColor: ['rgba(54, 162, 235, 1)'],
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