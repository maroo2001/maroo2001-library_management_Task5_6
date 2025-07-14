from odoo import models, fields, api

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)
    biography = fields.Text(string='Biography')  
    birth_date = fields.Date(string='Date of Birth') 
    nationality = fields.Char(string='Nationality')
    email = fields.Char(string='Email')

    book_ids = fields.One2many('library.book', 'author_id', string='Books')

    book_count = fields.Integer(string='Book Count', compute='_compute_book_count')

    @api.depends('book_ids')
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)
