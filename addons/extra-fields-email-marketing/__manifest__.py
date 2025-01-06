{
    'name': "Custom Mail Address",
    'summary': "Custom Mail Address",
    'version': '16.0.1.0.0',
    'website': "https://mcaf.nb.ca/en/",
    'author': "MCAF",
    'category': "Mail Address",
    'license': 'OPL-1',
    "application": True,
    "installable": True,
    'depends': ['base',
                'mass_mailing'],
    'data': [
        'views/custom_mail_address_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
