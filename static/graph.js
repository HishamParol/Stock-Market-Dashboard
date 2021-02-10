var data1 = {{dictionary.Signal}};
var data2 = {{dictionary.Moving_Avg}};
var labels1 = {{dictionary.labels}};

var ctx = document.getElementById('myChart').getContext('2d');
var mixedChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Closing Price',
            /*backgroundColor: 'rgb(255, 99, 132)',*/
            borderColor: 'rgb(255, 99, 132)',
            data: data1
        }, {
            label: 'Moving Average',
            borderWidth:3,
            borderColor:'rgb(0, 0, 255)',
            data: data2,

            // Changes this dataset to become a line
            type: 'line'
        }],
        labels: labels1
    },
    options: {
 scales: {
            yAxes: [{
               type: 'linear',
                ticks: {
                    beginAtZero:true
                }
            }],

            xAxes: [{
               distribution: 'linear',
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        plugins: {
            zoom: {
                // Container for pan options
                pan: {
                    // Boolean to enable panning
                    enabled: true,

                    // Panning directions. Remove the appropriate direction to disable 
                    // Eg. 'yy' would only allow panning in the y direction
                    mode: 'xy'
                },
                  // Container for zoom options
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,

                    // Zooming directions. Remove the appropriate direction to disable 
                    // Eg. 'y' would only allow zooming in the y direction
                    mode: 'xy',
                   sensitivity: 3,
                }

               
            }
        }
    }
        

});
    

