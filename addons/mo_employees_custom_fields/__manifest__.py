{
    'name': "HR Employee Custom Fields",
    'summary': "Custom HR Employee Information",
    'version': '16.0.1.2.0',
    'website': "https://mcaf.nb.ca/en/",
    'author': "MCAF",
    'category': "HR",
    'license': 'OPL-1',
    "application": True,
    "installable": True,
    'depends': ['base', 'hr', 'web', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'data/kron_data.xml',
        'data/hr_demo.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'data/update_timezone_action.xml',
        'data/employee_birthday_template.xml',
        'data/employee_90_days_confirm_template.xml',
        'data/employee_end_probation.xml',
        'data/employee_reminder_probation.xml',
        'data/employee_tier_update.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'mo_employees_custom_fields/static/src/js/custom_fields_validation.js',
        ],

    },
}
