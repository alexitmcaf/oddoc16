import re
from datetime import timedelta

from odoo import fields, models, api, _, exceptions


class CustomContactFields(models.Model):
    """Adding custom address
       fields"""
    _inherit = 'hr.employee'

    street_employee = fields.Char(string=' Street ', help='Street address')
    phone_employee = fields.Char(string=' Phone ',
                                 help='Phone number',
                                 readonly=False)
    city_employee = fields.Char(string=' City ', help='City')
    state_employee_id = fields.Many2one(
        'res.country.state',
        string='Province',
        default=lambda self: self.env['res.country.state'].search(
            [('code', '=', 'NB')], limit=1),
        help='Select the state for the contact.'
    )
    country_employee_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env['res.country'].search(
            [('code', '=', 'CA')], limit=1),
        help='Select the country for the contact.'
    )
    zip_code_employee = fields.Char(string=' Zip Code ',
                                    help='Zip Code')

    tier_employee = fields.Selection([
        ('no-tier', 'No-Tier'),
        ('1-tier', '1-Tier'),
        ('2-tier', '2-Tier'),
        ('3-tier', '3-Tier'),
        ('4-tier', '4-Tier')
    ], string="Teacher's Tiers", default='no-tier')

    email__employee = fields.Char(string="Email",
                                  help="Email address",
                                  readonly=False)

    @api.constrains('phone_employee', 'email__employee', 'zip_code_employee')
    def _check_employee_details(self):
        error_messages = []
        zip_code_pattern = re.compile(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$')
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        phone_pattern = re.compile(r'^(\d-?){9}\d$')
        for record in self:
            if record.phone_employee and not phone_pattern.match(record.phone_employee):
                error_messages.append(_('Phone: Invalid phone number. Please enter a 10-digit phone number'))

            if record.email__employee and not email_pattern.match(record.email__employee):
                error_messages.append(_('Email: Please enter a valid email address'))

            if record.zip_code_employee and not zip_code_pattern.match(record.zip_code_employee):
                error_messages.append(_('Zip Code: enter a valid postal code in format A1A 1A1'))

        if error_messages:
            raise exceptions.ValidationError('\n'.join(error_messages))

    @api.model
    def check_90_days_employment(self):
        today = fields.Date.today()
        ninety_days = today - timedelta(days=90)

        contract_histories = self.env['hr.contract.history'].search([('date_hired', '!=', False),
                                                                     ('date_hired', '=', ninety_days)])
        for history in contract_histories:
            employee = history.employee_id
            if employee:
                self.days_90_completion_email(employee)

    def days_90_completion_email(self, employee):
        template = self.env.ref('mo_employees_custom_fields.'
                                'email_template_90_days_completion')
        company_email = (employee.company_id.email or
                         self.env.user.company_id.email)
        parent_id_email = employee.parent_id.work_email
        hr_contract = self.env['hr.contract'].search([('employee_id', '=', employee.id)], limit=1)
        hr_responsible_email = hr_contract.hr_responsible_id.work_email if hr_contract else None

        if template:
            template.email_from = company_email
            email_list = []
            if parent_id_email:
                email_list.append(parent_id_email)
            if hr_responsible_email:
                email_list.append(hr_responsible_email)

            for email in email_list:
                template.email_to = email
                template.send_mail(employee.id, force_send=True,
                                   email_values={'email_to': email})

    @api.model
    def _check_birthdays(self):
        today = fields.Date.today()
        employees = self.env["hr.employee"].search([])
        for employee in employees:
            if (
                    employee.birthday
                    and employee.birthday.day == today.day
                    and employee.birthday.month == today.month
            ):

                template_employee_id = self.env.ref('mo_employees_custom_fields.'
                                                    'email_template_birthday')
                template_employee_id.send_mail(employee.id, force_send=True)
                template_coworker_id = self.env.ref('mo_employees_custom_fields.'
                                                    'email_template_coworkers')

                if len(employees) > 1:
                    for coworker in employees:
                        if coworker == employee:
                            continue
                        template_coworker_id.with_context(
                            birthday_employee=employee.name
                        ).send_mail(coworker.id, force_send=True)

    @api.model
    def check_tier_updates(self):
        employees = self.search([])

        for employee in employees:
            if (employee.contract_id and
                    employee.contract_id.probation_end_date):
                probation_end_date = fields.Date.from_string(employee.
                                                             contract_id.
                                                             probation_end_date)

                if probation_end_date == fields.Date.today():
                    # employee.tier_employee = '1-tier' for changing the tier
                    self.notify_hr_group(employee,
                                         "completed probation")

                unit_amounts = self.env['account.analytic.line'].search([
                    ('employee_id', '=', employee.id),
                    ('date', '>=', probation_end_date)
                ]).mapped('unit_amount')

                total_hours_after_probation = sum(unit_amounts)

                if (total_hours_after_probation >= 800 and
                        employee.tier_employee == '1-tier'):
                    self.notify_hr_group(employee,
                                         "reached 800 hours after probation")
                elif (total_hours_after_probation >= 2300 and
                      employee.tier_employee == '2-tier'):
                    self.notify_hr_group(employee,
                                         "reached 2300 hours after probation")
                elif (total_hours_after_probation >= 3800 and
                      employee.tier_employee == '3-tier'):
                    self.notify_hr_group(employee,
                                         "reached 3800 hours after probation")

    def notify_hr_group(self, employee, message):

        template = self.env.ref('mo_employees_custom_fields.'
                                'email_template_employee_tier_change')
        company_email = (employee.company_id.email or
                         self.env.user.company_id.email)
        parent_id_email = employee.parent_id.work_email
        hr_contract = self.env['hr.contract'].search([('employee_id', '=', employee.id)], limit=1)
        hr_responsible_email = hr_contract.hr_responsible_id.work_email if hr_contract else None

        if template:
            template.email_from = company_email
            email_list = []

            if parent_id_email:
                email_list.append(parent_id_email)
            if hr_responsible_email:
                email_list.append(hr_responsible_email)

            for email in email_list:
                email_subject = _("Tier Update Notification: {}").format(message)
                template.send_mail(employee.id, force_send=True,
                                   email_values={'email_to': email, 'subject': email_subject})


class CustomHrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    resource_calendar_id = fields.Many2one(
        'resource.calendar',
        string='Budget',
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]"
    )

    tz = fields.Selection(
        string='Timezone', related='resource_id.tz', readonly=False,
        default='Canada/Atlantic',
        help="This field is used in order "
             "to define in which timezone "
             "the resources will work.")
