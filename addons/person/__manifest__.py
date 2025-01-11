{
    'name': 'Person and Client Management',
    'version': '16.0.1.0.0',
    'summary': 'Manage information about persons and clients',
    'author': 'MCAF',
    'website': 'https://www.test.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/custom_client_view.xml',

    ],
    'images': [
        'static/description/icon.png',
    ],
}