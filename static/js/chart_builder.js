var chart;

function buildChart(id, url, label) {
    $.ajax({
        url: url,
        method: "GET",
        dataType: 'JSON',
        success: function (data) {
            console.log(data);
            let region = data.region;
            let value = data.value;

            // For attending charts
            const avValue = value.reduce((a, b) => (a + b)) / value.length;
            let color;
            if(avValue >= 75) color = '#2ECC71'
            else if(avValue <= 50) color = '#e66767'
            else color = '#FBC02D'

            const chartdata = {
                labels: region,
                datasets: [
                    {
                        label: label,
                        backgroundColor: color,
                        borderColor: color,
                        hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
                        hoverBorderColor: 'rgba(200, 200, 200, 1)',
                        lineTension: 0,                                // Linear interpolation
                        data: value.map(function (x) {
                            return x * 1;
                        })
                    }
                ]
            };

            const ctx = $("#" + id);

            chart = new Chart(ctx, {
                type: 'line',
                data: chartdata,
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                display: false,
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                max: 100
                            }
                        }]
                    }
                }
            });
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function updateChart() {
    chart.update();
}