{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Manage library books and authors',
    'category': 'Tools',
    'author': 'Maryam',

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_author_views.xml',
        'views/library_book_views.xml',
        'views/library_borrow_views.xml',
    ],
    'installable': True,
    'application': True,
}

