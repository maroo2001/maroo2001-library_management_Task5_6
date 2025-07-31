from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_ids = fields.One2many('library.membership', 'partner_id', string='Library Memberships')
    membership_count = fields.Integer(string='Membership Count', compute='_compute_membership_count')
    card_id = fields.Char(string='Card ID', readonly=True, copy=False)

    def _compute_membership_count(self):
        for partner in self:
            partner.membership_count = len(partner.membership_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('card_id'):
                # توليد card_id باستخدام ir.sequence (الطريقة الصحيحة)
                vals['card_id'] = self.env['ir.sequence'].next_by_code('library.card.id') or 'CARD-0000'
        return super().create(vals_list)
