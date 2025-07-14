from odoo import models, fields, api
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
        """Mark the borrowing as returned."""
        for record in self:
            if not record.returned:
                record.returned = True

    # ==== Default Values ====
    @api.model
    def default_get(self, fields):
        """Auto-fill return_date if not manually set."""
        res = super().default_get(fields)
        if 'borrow_date' in res and not res.get('return_date'):
            res['return_date'] = res['borrow_date'] + timedelta(days=7)
        return res
