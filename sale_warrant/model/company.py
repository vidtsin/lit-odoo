# -*- coding: utf-8 -*-
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
#

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    # default_sale_order_validity_days = fields.Integer(
    #     string="Default Warrant Period of Sale Orders (in days)",
    #     help="By default, the warrant period of sale orders will be "
    #          "the date of the sale order plus the number of days defined "
    #          "in this field. If the value of this field is 0, the sale orders "
    #          "will not have a validity date by default.")

    # _sql_constraints = [
    #     ('sale_order_validity_days_positive',
    #      'CHECK (default_sale_order_validity_days >= 0)',
    #      "The value of the field 'Default Validity Duration of Sale Orders' "
    #      "must be positive or 0."),
    # ]

    default_sale_order_warrant_period = fields.Char(
        string="Default Warrant Period of Sale Orders",
        help="By default, this warrant period of sale orders will be "
             "copied in sale order field "
             "If the value of this field is blank, the sale orders "
             "will not have a warrant period by default.")
