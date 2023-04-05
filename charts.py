from app import date_range, list_values_NAV

data = {
    'labels': date_range.to_list(),
    'datasets': [
        {
            'label': 'NAV points',
            'data': list_values_NAV,
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'lineTension': 0.1
        }
    ]
}

options = {
    'scales': {
        'yAxes': [{
            'ticks': {
                'beginAtZero': True
            }
        }]
    }
}

nav_chart = Chart('myChart', {'type': 'line', 'data': data, 'options': options})
