# -*- coding: utf-8 -*-
{
    'name': "Hielos Custom Liderit",

    'summary': """
        Customization for Hielos""",

    'description': """
        Create field cliente_europastry  
    """,

    'author': "Lider IT",
    'website': "http://www.liderit.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner.xml',
    ],
    
}