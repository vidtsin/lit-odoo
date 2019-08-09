# -*- coding: utf-8 -*-
from openerp import models, api


class sale_order_batch_confirm(models.TransientModel):
    _name = 'sale.batch.confirm'

    @api.multi
    def batch_confirm_so(self):
        active_ids = self.env.context.get('active_ids', [])
        SaleOrders = self.env['sale.order'].search([('id', 'in', active_ids), ('state', '=', 'draft')])
        for SaleOrder in SaleOrders:
            SaleOrder.action_button_confirm()
