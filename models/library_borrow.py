from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Borrowing Record'

    # ==== Fields ====
    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date', store=True)
    returned = fields.Boolean(string='Returned', default=False)

    # ==== Onchange Logic ====
    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        """Auto-fill return date as 7 days after borrow date."""
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    # ==== Mark as Returned ====
    def action_mark_returned(self):
        """Mark the borrowing as returned and make book available."""
        for record in self:
            if not record.returned:
                record.returned = True
                # جعل الكتاب متاحًا بعد الإرجاع
                record.book_id._compute_is_available()

    # ==== Default Values ====
    @api.model
    def default_get(self, fields):
        """Auto-fill return_date if not manually set."""
        res = super().default_get(fields)
        if 'borrow_date' in res and not res.get('return_date'):
            res['return_date'] = res['borrow_date'] + timedelta(days=7)
        return res


    # ==== Create Override ====
    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            book_id = vals.get('book_id')
            if book_id:
                existing_borrow = self.search([
                    ('book_id', '=', book_id),
                    ('returned', '=', False)
                ], limit=1)
                if existing_borrow:
                    raise ValidationError("This book is currently borrowed and not returned yet.")

            # 🔐 التحقق من البطاقة والعضوية
            partner_id = vals.get('borrower_id')
            partner = self.env['res.partner'].browse(partner_id)
            if not partner.card_id:
                raise ValidationError("User does not have a valid card.")

            active_membership = self.env['library.membership'].search([
                ('partner_id', '=', partner_id),
                ('registration_date', '<=', fields.Date.today()),
                ('end_date', '>=', fields.Date.today()),
                ('active', '=', True),
            ], limit=1)

            if not active_membership:
                raise ValidationError("User must have an active membership.")
        
        return super().create(vals_list)
