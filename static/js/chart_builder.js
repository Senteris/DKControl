function buildChart(id, url, label) {
    $.ajax({
        url: url,
        method: "GET",
        dataType: 'JSON',
        success: function (data) {
            console.log(data);
            let region = data.region;
            let value = data.value;

            var chartdata = {
                labels: region,
                datasets: [
                    {
                        label: label,
                        backgroundColor: 'rgba(200, 200, 200, 0.75)',
                        borderColor: 'rgba(200, 200, 200, 0.75)',
                        hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
                        hoverBorderColor: 'rgba(200, 200, 200, 1)',
                        data: value.map(function (x) {
                            return x * 1;
                        })
                    }
                ]
            };

            var ctx = $("#" + id);

            var barGraph = new Chart(ctx, {
                type: 'bar',
                data: chartdata,
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
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
