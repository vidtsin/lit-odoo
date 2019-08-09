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

from odoo import fields, models,api
from odoo.addons import decimal_precision as dp

import logging 
_logger = logging.getLogger(__name__)

class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    def product_id_change(self,pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = super(sale_order_line, self).product_id_change(pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag)
        if not pricelist:
            return res
        if context is None:
            context = {}
        frm_cur = self.env['res.users'].browse().company_id.currency_id.id
        to_cur = self.env['product.pricelist'].browse([pricelist])[0].currency_id.id
        if product:
            product = self.env['product.product'].browse(product)
            purchase_price = product.standard_price
            to_uom = res.get('product_uom', uom)
            if to_uom != product.uom_id.id:
                purchase_price = self.env['product.uom']._compute_price(product.uom_id.id, purchase_price, to_uom)
            ctx = context.copy()
            ctx['date'] = date_order
            price = self.env['res.currency'].compute(frm_cur, to_cur, purchase_price, round=False, context=ctx)
            res['value'].update({'purchase_price': price})
        return res

    def _product_margin_uom(self,field_name, arg):
        cur_obj = self.env['res.currency']
        #_logger.error('##### AIKO ###### Entro en sale_margin_uom para recalcular margenes por linea')
        res = {}
        for line in self.browse():
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = 0
            if line.product_id:
                tmp_margin = line.price_subtotal - ((line.purchase_price or line.product_id.standard_price) * line.product_uom_qty)
                #_logger.error('##### AIKO ###### Sale_margin_uom para recalcular margenes en la linea %s'%line)
                #_logger.error('##### AIKO ###### Sale_margin_uom para recalcular margenes con valor %s'%tmp_margin)
                res[line.id] = cur_obj.round(cur, tmp_margin)
        return res

    margin = fields.Float(string="Margin",compute="_product_margin_uom",digits_compute= dp.get_precision('Product Price'),stor=True)
    purchase_price = fields.Float(string="Cost Price",digits_compute= dp.get_precision('Product Price'))

class sale_order(models.Model):
    _inherit = "sale.order"

    def _product_margin(self,*args,**kwargs):
        result = {}
        for sale in self.browse():
            result[sale.id] = 0.0
            for line in sale.order_line:
                if line.state == 'cancel':
                    continue
                result[sale.id] += line.margin or 0.0
        return result

    def _get_order(self):
        result = {}
        for line in self.env['sale.order.line'].browse():
            result[line.order_id.id] = True
        return result.keys()

    margin = fields.Float(string="Margin",compute="_product_margin", help="It gives profitability by calculating the difference between the Unit Price and the cost price.", store={
                'sale.order.line': (compute="_get_order", ['margin', 'purchase_price', 'order_id'], 20),
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 20),
                }, digits= dp.get_precision('Product Price'))
