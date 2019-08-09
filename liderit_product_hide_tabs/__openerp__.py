# -*- coding: utf-8 -*-

{
    'name': 'Lider IT Product Hide Tabs',
    'version': '9.0.0.1.0',
    'category': 'Products',
    'sequence': 14,
    'summary': 'Invoicing, Commercial, Partners',
    'description': """
Lider IT Product Hide Tabs
==========================
This is a security feature, in order to hide all tabs, except Information, in product
form view for all user groups except for stock manager.
Set product type to read only in view and hide  product category.
    """,
    'author':  'Lider IT',
    'website': 'https://liderit.es',
    'images': [
    ],
    'depends': [
        'stock',
        'stock_account',
        'account'
    ],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}