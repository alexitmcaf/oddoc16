from odoo import fields, models


class CustomMailAddress(models.Model):
    """Adding custom address
       fields"""
    _inherit = 'mailing.contact'

    street = fields.Char(string=' Street ',
                         required=True,
                         help='Street address')
    city = fields.Char(string=' City ',
                       required=True,
                       help='City')
    state_id = fields.Many2one(
        'res.country.state',
        string='Province',
        default=lambda self: self.env['res.country.state'].search([('code', '=', 'NB')], limit=1),
        help='Select the state for the contact.'
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env['res.country'].search([('code', '=', 'CA')], limit=1),
        help='Select the country for the contact.'
    )
    zip_code = fields.Char(string=' Zip Code ',
                           required=True,
                           help='Zip Code')
