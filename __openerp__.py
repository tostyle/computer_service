# -*- coding: utf-8 -*-
{
    'name': "ComputerService",

    'summary': """
        Service of Request from Receive & Return Computer with little computer assest management""",

    'description': """
        Request for receive and return computer
    """,
    'css': ['static/src/css/custom.css'],
    'author': "Tostyle",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report'],

    # always loaded
    'data': [
        'views/menu.xml',
        'views/views.xml',
        'views/form.xml',
        'views/tree.xml',
        'views/search.xml',
        'views/resource.xml',
        'views/sequence.xml',
        'views/report.xml',
        'views/receive_print_form.xml',
        'views/summary_report.xml',
        'views/serial_search_report.xml',
        'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
