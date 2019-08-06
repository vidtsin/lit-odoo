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

from openerp import models, fields, api


class pricelist_partnerinfo(models.Model):
    _inherit = 'pricelist.partnerinfo'

    partner = fields.Many2one(
        comodel_name='res.partner', string='Partner',
        related='suppinfo_id.name', store=True)
    type = fields.Selection(
        string='Type', related='suppinfo_id.type', store=True)
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product Template',
        related='suppinfo_id.product_tmpl_id', store=True)
    product_name = fields.Char(
        string='Product Name', related='suppinfo_id.product_name', store=True)
    product_code = fields.Char(
        string='Product Code', related='suppinfo_id.product_code', store=True)
    product_cost = fields.Float(
        string='Product Cost', related='product_tmpl_id.standard_price')
    product_pricelist = fields.Float(
        string='Product Price List', related='product_tmpl_id.list_price')
    product_uom_po = fields.Char(
        string='Purchase UOM', related='product_tmpl_id.uom_po_id.name')
    sequence = fields.Integer(
        string='Sequence', related='suppinfo_id.sequence', store=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        related='suppinfo_id.company_id', store=True)
    net_price = fields.Float (compute = '_get_net_price')


    @api.one
    def _get_net_price(self):

        self.net_price = self.price * ((100-self.discount) /100)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
