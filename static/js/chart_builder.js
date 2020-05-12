$(document).ready(function(){
    $.ajax({
        url: "http://your_way",
        method: "GET",
        dataType : 'JSON',
        success: function(data) {
            console.log(data);
            let region = [];
            let value = [];

            for (let i in data) {
                region.push(data[i].CHART_NAME);
                value.push(data[i].REQ_VALUE);
            }

            var chartdata = {
                labels: region,
                datasets : [
                    {
                        label: 'Region',
                        backgroundColor: 'rgba(200, 200, 200, 0.75)',
                        borderColor: 'rgba(200, 200, 200, 0.75)',
                        hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
                        hoverBorderColor: 'rgba(200, 200, 200, 1)',
                        data: value.map(function(x) {return x * 1;})
                    }
                ]
            };

            var ctx = $("#chart_id");

            var barGraph = new Chart(ctx, {
                type: 'bar',
                data: chartdata
            });
        },
        error: function(data) {
            console.log(data);
        }
    });
});
