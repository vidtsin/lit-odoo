# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Sale Link module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Account Invoice Change Due',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Modify dues dates',
    'description': """
Account Invoice Change Dues
============================

On the customer invoices, you can see now dues and change them. 

    """,
    'author': 'Lider IT',
    'website': 'http://www.liderit.es',
    'depends': ['account','account_due_list','account_due_list_payment_mode'],
    'data': ['account_invoice_view.xml'],
    'installable': True,
    'active': False,
}
