# -*- coding: utf-8 -*-
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

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _get_sale_id(self,name,args):
        #ampliamos la funcion por el posible registro en lineas de venta del destino de cada linea (proc_group)
        res = {}
        for picking in self:
            sale_obj = self.env['sale.order'].search([('procurement_group_id','=',picking.group_id.id)])
            if sale_obj:
                res[picking.id] = sale_obj[0]
            else:
                sale_line_obj = self.env['sale.order.line'].search([('procurement_group_id','=',picking.group_id.id)])
                if sale_line_obj:
                        res[picking.id] = sale_line_obj[0]
        return res


    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        # _logger.error('######## AIKO entro en create invoice form picking para plazos y modos de pago')
        if picking and picking.group_id:
            sale_obj = self.env['sale.order.line'].search([('procurement_group_id','=',picking.group_id.id)])
            if sale_obj:
                sale_id = sale_obj[0].order_id.id
                pick_sale = self.env['sale.order'].search([('id','=',sale_id)])
                # _logger.error('######## AIKO _create_invoice_from_picking valor de pick_sale  %s'%pick_sale)
                if pick_sale:
                    th_sale = pick_sale[0]
                    # _logger.error('######## AIKO _create_invoice_from_picking valor de payterm es  %s'%th_sale.payment_term)
                    # _logger.error('######## AIKO _create_invoice_from_picking valor de paymode es  %s'%th_sale.payment_mode_id)
                    if th_sale.payment_term:
                        vals['payment_term'] = th_sale.payment_term.id
                    if th_sale.payment_mode_id:
                        vals['payment_mode_id'] = th_sale.payment_mode_id.id

        return super(StockPicking, self)._create_invoice_from_picking(picking,vals)
