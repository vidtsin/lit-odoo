#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Accesibility',
    'author': 'LIDER IT',
    'version': '1.0',
    'category': 'Web',
    'sequence': 6,
    'summary': '',
    'description': """

=======================


""",
    'depends': ['web'],
    'data': [
        'views/templates.xml','views/views.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
}
