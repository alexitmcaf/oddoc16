from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class CustomClient(models.Model):
    _name = 'custom.client'
    _description = 'Model of a client'
    _inherit = 'abstract.person'

    photo = fields.Binary(string="Photo")
    postalcode = fields.Char(string="Postal Code")

    @api.constrains('postalcode')
    def _check_postalcode(self):
        for record in self:
            if record.postalcode:
                if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', record.postalcode):
                    raise ValidationError("Postal Code must be in the format A1A 1A1.")



