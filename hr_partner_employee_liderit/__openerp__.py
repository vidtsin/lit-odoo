# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
    'name'          : 'HR - Partner / Employee for LiderIT',
	'version'       : '1.0',
	'category'      : 'Human Resources',
	'summary'       : 'Creates an employee out of a partner',
	'description'   : """
Deals with the connection between Partners and Employees\n\n
- one can create an employee from the partner's form\n
- shows the 'employee' field in the partner's form (readonly)\n
                        
                        """,
	'author'        : 'LiderIT',
	'website'       : 'http://www.liderit.es',
	'depends'       : ['hr'],
	'data'          : ['hr_partner_employee_view.xml'],
    'installable'   : True,
    'active'        : False,
}
