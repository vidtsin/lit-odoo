# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    MERGE_STATES = ['draft', 'sent', 'confirm', 'waiting_date',
                    'progress', 'manual','done']


    @api.multi
    def _can_merge(self):
        """ Hook for redefining merge conditions """
        self.ensure_one()
        return self.state in self.MERGE_STATES and self.order_line
        

    @api.multi
    def _get_merge_domain(self):
        """ Hook for redefining merge conditions """
        policy_clause = []
        if self.state not in ('draft', 'sent'):
            policy_clause = [
                '|', ('order_policy', '=', self.order_policy),
                ('state', 'in', ('draft', 'sent'))]
        return [
            ('id', '!=', self.id),
            ('partner_id', '=', self.partner_id.id),
            ('partner_shipping_id', '=', self.partner_shipping_id.id),
            ('warehouse_id', '=', self.warehouse_id.id),
            ('company_id', '=', self.company_id.id),
            ('state', 'in', self.MERGE_STATES),
        ] + policy_clause
