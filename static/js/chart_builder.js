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

            let color;
            // For attending charts
            if (value.length != 0) {
                const avValue = value.reduce((a, b) => (a + b)) / value.length;

                if (avValue >= 75) color = '#2ECC71'
                else if (avValue <= 50) color = '#e66767'
                else color = '#FBC02D'
            }
            else color = '#ffffff'

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
                    maintainAspectRatio: false,
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
            chart.canvas.parentNode.style.height = '275px';
            chart.canvas.parentNode.style.width = '500px';
        },
        error: function (data) {
            console.log(data);
        }
    });
}