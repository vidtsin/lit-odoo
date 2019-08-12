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

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

import logging 
_logger = logging.getLogger(__name__)

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def _product_margin_uom(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        #_logger.error('##### AIKO ###### Entro en sale_margin_uom para recalcular margenes por linea')
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = 0
            if line.product_id:
                tmp_margin = line.price_subtotal - ((line.purchase_price or line.product_id.standard_price) * line.product_uom_qty)
                #_logger.error('##### AIKO ###### Sale_margin_uom para recalcular margenes en la linea %s'%line)
                #_logger.error('##### AIKO ###### Sale_margin_uom para recalcular margenes con valor %s'%tmp_margin)
                res[line.id] = cur_obj.round(cr, uid, cur, tmp_margin)
        return res

    _columns = {
        'margin': fields.function(_product_margin_uom, string='Margin', digits_compute= dp.get_precision('Product Price'),
              store = True),
    }