from email.policy import default
from odoo import models,fields,api

class Dep(models.Model):
       _name = 'zeyna.detail'
     
       name = fields.Selection([('odepo', 'ODEPO'), ('unik', 'UNIK'), ('zeyna', 'ZEYNA')], default="fcfa", string="Ripositorie", required=True)
       branche= fields.Char(string="Branche", required=True)
     