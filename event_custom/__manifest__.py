# -*- coding: utf-8 -*-

{
    'name': 'Event Customization',
    'version': '17.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Event Customization',
    'description': """Event Customization""",
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['event_ticket_qr_scanner', 'website_event_track', 'event'],
    'data': [
        'data/data.xml',
        'views/event_event_views.xml',
        'views/event_event_reports.xml',
        'views/ir_actions_report.xml',
    ],
        'assets': {
        'web.assets_backend': [
            'event_custom/static/src/js/qweb_action_manager.js',
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
