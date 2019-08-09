# -*- coding: utf-8 -*-
{
    'name': "sincronizacion Europastry",

    'summary': """
        Integracion con el sistema de importacion/exportacion de ficheros de Europastry""",

    'description': """
        Integracion con el sistema de importacion/exportacion de ficheros de Europastry
    """,

    'author': "Fran Vega, LiderIT",
    'website': "https://www.liderit.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','hielos_custom_liderit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/europastry.xml',
        'views/europastry_pedidos.xml',
        'wizard/wizard.xml',
        'data/europastry_informe_file.xml',
        'data/europastry_informe.xml',
    ],
    
}