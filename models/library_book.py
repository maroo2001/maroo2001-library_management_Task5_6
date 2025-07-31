from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author')
    description = fields.Text(string='Description')
    publish_date = fields.Date(string='Publish Date')

    borrowing_ids = fields.One2many('library.borrowing', 'book_id', string='Borrowings')

    is_available = fields.Boolean(
        string='Available',
        compute='_compute_is_available',
        store=True
    )

    @api.depends('borrowing_ids.returned')
    def _compute_is_available(self):
        for book in self:
            active_borrowings = book.borrowing_ids.filtered(lambda b: not b.returned)
            book.is_available = len(active_borrowings) == 0
