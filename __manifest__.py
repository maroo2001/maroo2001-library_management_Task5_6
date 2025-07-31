{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Manage library books and authors',
    'category': 'Tools',
    'author': 'Maryam',
    'license': 'LGPL-3',

    'depends': ['base', 'product', 'account'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/library_author_views.xml',
        'views/library_book_views.xml',
        'views/library_borrow_views.xml',
        'views/library_partner_views.xml',
        'views/library_member_views.xml',
        'views/membership_request_views.xml',
        'data/library_sequence.xml', 
        'views/invoice_views.xml',
    

    ],
    'installable': True,
    'application': True,
}

