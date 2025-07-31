from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership'

    user_id = fields.Many2one('res.users', string="Responsible User")
    partner_id = fields.Many2one('res.partner', string="Member", required=True)
    card_id = fields.Char(related='partner_id.card_id', string="Card ID", readonly=True)
    registration_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    membership_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('student', 'Student'),
        ('vip', 'VIP'),
    ], string="Membership Type", required=True, default='monthly')
    active = fields.Boolean(default=True)
    note = fields.Text(string="Notes")

    @api.constrains('partner_id')
    def _check_active_membership(self):
        for record in self:
            active_memberships = self.search([
                ('partner_id', '=', record.partner_id.id),
                ('active', '=', True),
                ('id', '!=', record.id)
            ])
            if active_memberships:
                raise ValidationError("This member already has an active membership. You cannot add another until the current one ends.")

class MembershipLine(models.Model):
    _name = 'library.membership.line'
    _description = 'Membership Line'

    request_id = fields.Many2one('library.membership.request', string="Request", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    amount = fields.Float(string="Amount", required=True)
