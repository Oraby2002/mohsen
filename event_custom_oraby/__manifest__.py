{
    'name': 'Event Custom Oraby',
    'version': '1.0',
    'summary': 'Customizations for Event Module',
    'depends': ['event','event_custom'],
    'data': [
        'views/event_registration_view.xml',
        # 'views/event_registration_search.xml',
        'report/report_for_attented_list.xml',
    ],
    'installable': True,
    'application': False,
}
