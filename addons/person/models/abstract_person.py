from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Person(models.AbstractModel):
    _name = 'abstract.person'
    _description = 'Abstract model of a person'

    name = fields.Char(string='Name')
    telephone = fields.Char(string='Telephone')
    address = fields.Char(string='Address')
    email = fields.Char(string='Email')
    photo = fields.Binary(string='Photo', attachment=True)
    photo_filename = fields.Char(string="Photo Filename")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')

    @api.constrains('telephone')
    def _check_telephone(self):
        for record in self:
            if record.telephone and not re.match(r'^\d{10}$', record.telephone):
                raise ValidationError("Telephone must be a 10-digit number.")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.email):
                raise ValidationError("Email must be a valid email address.")
