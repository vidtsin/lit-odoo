# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2014 Apertoso NV (<http://www.apertoso.be>).
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

from openerp import fields, models, exceptions, api
from openerp.tools.translate import _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    require_customer = fields.Boolean(
        string='Cliente Requerido',
        help='Cliente Requerido en pedidos TPV')
    default_customer_id = fields.Many2one('res.partner', string='Cliente por defecto')
    
    _defaults = {
        'require_customer': False,
        } 

class PosOrder(models.Model):
    _inherit = 'pos.order'

    require_customer = fields.Boolean(
        string='Cliente Requerido',
        related='session_id.config_id.require_customer', readonly=True)

    @api.one
    @api.constrains('partner_id', 'require_customer')
    def _check_partner(self):
        if self.require_customer and not self.partner_id:
            raise exceptions.ValidationError(
                _('Cliente requerido para este pedido'))
