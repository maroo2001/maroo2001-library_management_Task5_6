from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    user_membership_count = fields.Integer(
        related='partner_id.membership_count',
        string='Membership Count',
        readonly=True,
        store=True
    )