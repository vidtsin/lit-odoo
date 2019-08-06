# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 Pexego (<www.pexego.es>). All Rights Reserved
#    $Omar Castiñeira Saavedra$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Creates prodlot sequence chooose product sequence"""

from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class StockProductionLot(models.Model):

    _inherit = "stock.production.lot"

    @api.model
    def make_sscc(self):
        """return production lot number"""
        if 'in_pick' in self._context.keys():
            return ''
        seq_obj = self.env['ir.sequence']
        sequence_id = self.env.ref('stock.sequence_production_lots').id

        
        product_id = self._context.get('product_id', False) or \
            self._context.get('default_product_id', False)
        partner_id = self._context.get('partner_id', False)
        _logger.error('########### Valor de context: %s', self._context)
        _logger.error('########### Valor de partner_id: %s', partner_id)
        product = self.env['product.product'].browse(product_id)

        if product and product.sequence_id:
            _logger.error('########### Producto con secuencia')
            if partner_id and product.ext_sequence_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.partner_type_id.name != 'G10 Paciente':
                    sequence_id = product.ext_sequence_id.id
                else:
                    sequence_id = product.sequence_id.id

            else:
                sequence_id = product.sequence_id.id

        _logger.error('########### Valor de sequence_id: %s', sequence_id)
        sequence = seq_obj.get_id(sequence_id)
        return sequence

    _defaults = {
        'name': make_sscc
    }

