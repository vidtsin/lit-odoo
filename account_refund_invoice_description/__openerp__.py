# -*- encoding: utf-8 -*-
##############################################################################
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
    'name': 'Refund Description Field',
    'version': '0.1',
    'category': 'Account',
    'license': 'AGPL-3',
    'summary': 'Display the field descripction in refund invoices',
    'description': """
Stock Display Sale ID
=====================

Display the field descripction in refund invoices in order to edit it.


    """,
    'author': 'Lider IT',
    'website': 'http://www.liderit.es',
    'depends': ['account','account_refund_original'],
    'data': ['account_refund_view.xml'],
    'installable': True,
    'active': False,
}
