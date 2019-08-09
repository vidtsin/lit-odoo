# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp

import logging
logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    """Add the computation for the stock available to promise"""
    _inherit = 'product.product'

    min_stock_qty = fields.Float(
        compute='_get_min_stock_qty',
        type='float',
        digits_compute=dp.get_precision('Product Unit of Measure'),
        string='Min Stock Qty',
        )


    @api.multi
    def _get_min_stock_qty(self):
        """Compute the quantities in Quotations."""

        env_op = self.env['stock.warehouse.orderpoint']
        for p in self:
            if p.orderpoint_ids:
                ops = []
                for op in p.orderpoint_ids:
                    ops.append (op.id)
                op_src = env_op.search([('id','in',ops)],order='product_min_qty asc',limit=1)
                # logger.error('Valor para op_src tras search %s'%op_src)

                p.min_stock_qty = op_src[0].product_min_qty


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_stock_qty = fields.Float(
        compute='_get_min_stock_qty',
        type='float',
        digits_compute=dp.get_precision('Product Unit of Measure'),
        string='Min Stock Qty',
        )

    @api.multi
    @api.depends('product_variant_ids.min_stock_qty')
    def _get_min_stock_qty(self):
        """Compute the quantity using all the variants"""
        for tmpl in self:
            tmpl.min_stock_qty = min(
                [v.min_stock_qty for v in tmpl.product_variant_ids])



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'



    immediately_usable_qty = fields.Float(related='product_id.immediately_usable_qty', string='Available to promise')
    min_stock_qty = fields.Float(related='product_id.min_stock_qty',string='Min Stock Quantity')

