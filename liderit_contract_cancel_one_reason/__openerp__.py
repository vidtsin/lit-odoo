# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
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
    'name': 'Lider IT Contract Termination Reasons',
    'version': '1.0',
    'category': 'Reasons',
    'summary': 'Manage One Termination Reason in Contracts',
    'description': """
	Lets you define and choose one termination reason for Contracts.
    Uses base_reason module as a base for reason management. Termination reasons become visible
    when contract end date is specified.
	""",
    'author': 'OERP / Lider IT',
    'website': 'www.liderit.es',
    'depends': [
        'base_reason', 'account', 'hr_timesheet_invoice'      
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/analytic_view.xml',
        #'data/,        

    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
