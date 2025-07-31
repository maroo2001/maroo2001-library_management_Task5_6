from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryMembershipRequest(models.Model):
    _name = 'library.membership.request'
    _description = 'Library Membership Request'

    partner_id = fields.Many2one('res.partner', string="Member", required=True)
    card_id = fields.Char(string="Card ID", readonly=True)
    registration_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    payment_terms = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ], string="Payment Terms")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('active', 'Active'),
    ], string="Status", default='draft', readonly=True, copy=False)

    line_ids = fields.One2many('library.membership.line', 'request_id', string="Membership Lines")
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft requests can be confirmed.")
            if not record.line_ids:
                raise ValidationError("You must add at least one membership line.")

            invoice_lines = []
            for line in record.line_ids:
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': 1,
                    'price_unit': line.amount,
                    'name': line.product_id.name,
                    'account_id': line.product_id.property_account_income_id.id or line.product_id.categ_id.property_account_income_categ_id.id,
                }))

            invoice = self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines,
            })

            record.invoice_id = invoice.id
            record.state = 'confirmed'

    def action_mark_paid(self):
        for record in self:
            if record.state != 'confirmed':
                raise ValidationError("Only confirmed requests can be marked as paid.")

            if not record.invoice_id or record.invoice_id.payment_state != 'paid':
                raise ValidationError("Invoice is not paid yet.")

            record.card_id = f"CARD{record.id:04d}"
            record.partner_id.card_id = record.card_id
            record.state = 'active'

    @api.constrains('partner_id')
    def _check_active_membership_request(self):
        for record in self:
            existing = self.search([
                ('partner_id', '=', record.partner_id.id),
                ('state', 'in', ['draft', 'confirmed', 'paid', 'active']),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError("This member already has an active or pending membership request.")
