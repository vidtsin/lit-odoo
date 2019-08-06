# -*- coding: utf-8 -*-
{
    'name': 'Debt notebook Liderit (technical core)',
    'version': '2.0.0',
    'author': 'IT-Projects LLC, Ivan Yelizariev',
    'summary': 'Debt payment method for POS',
    'license': 'GPL-3',
    'category': 'Point Of Sale',
    'website': 'https://it-projects.info',
    'depends': ['point_of_sale', 'account'],
    'data': [
        'data.xml',
        'views.xml',
        ],
    'installable': True,
    'post_init_hook': 'init_debt_journal',
}
