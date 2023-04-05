var ctx = document.getElementById('myChart');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [{% for item in content.date_range_no_datetime %}
            "{{item}}",
            {% endfor %}],
        datasets: [{
            label: 'You',
            data: [{% for item in content.list_values_NAV %}
                "{{item}}",
                {% endfor %}],
            borderWidth: 2,
            borderColor: 'purple',
            backgroundColor: 'rgba(47, 47, 47, 0.2)',
            pointBackgroundColor: 'purple',
            pointBorderColor: '#fff',
            pointBorderWidth: 1,
            pointRadius: 5,
            pointHoverRadius: 8
        },
        {
            label: 'Benchmark',
            data: [{% for item in content.list_values_SP500 %}
                "{{item}}",
                {% endfor %}],
            borderWidth: 1,
            borderColor: '#2f2f2f',
            backgroundColor: 'rgba(47, 47, 47, 0.2)',
            pointBackgroundColor: '#2f2f2f',
            pointBorderColor: '#fff',
            pointBorderWidth: 1,
            pointRadius: 5,
            pointHoverRadius: 8
        }
    ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: false,
                ticks: {
                    font: {
                        family: 'Roboto',
                        size: 14
                    }
                }
            },
            x: {
                ticks: {
                    font: {
                        family: 'Roboto',
                        size: 14
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Roboto',
                        size: 14
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true
    }
});