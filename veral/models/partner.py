# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################


from openerp import models, fields, api

from dateutil.relativedelta import *
from datetime import date, datetime

import logging
logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = 'res.partner'


    parque_lines = fields.One2many('veral.partner.product', 'partner_id', 'Parque del cliente')
    fecha_alta = fields.Char('Año de Alta')
    no_marketing = fields.Boolean ('No activo para marketing')



class veral_partner_product(models.Model):
    _name = 'veral.partner.product'

    name = fields.Char('Parque')
    partner_id = fields.Many2one ('res.partner','Empresa')
    # date = fields.Char('Año', default=lambda self: fields.Date.today())
    date = fields.Char('Año', default=lambda self: datetime.now().year)
    baja = fields.Char('Año de Baja')
    notas = fields.Text('Notas')
    subproduct_id = fields.Many2one ('veral.product.subtype','Tipo de Máquina')


class veral_product_type(models.Model):
    _name = 'veral.product.type'

    name = fields.Char('Clase de Máquina')
    # usadas = fields.Boolean(string='Gestionar Usadas', default=False)


class veral_product_subtype(models.Model):
    _name = 'veral.product.subtype'

    name = fields.Char('Tipo de Máquina')
    product_type = fields.Many2one ('veral.product.type','Clase de Máquina')
    estado = fields.Selection([('Nueva', 'Nueva'), ('Usada', 'Usada')],"Estado máquina", default="N")


    @api.multi
    @api.depends('name', 'product_type', 'estado')
    def name_get(self):
        result = []
        for prod in self:
            result.append((prod.id, '%s %s %s' % (prod.product_type.name,prod.name,prod.estado)))
        return result

class crm_case_stage(models.Model):
    _inherit = 'crm.case.stage'

    no_marketing = fields.Boolean ('No activo para marketing')



class crm_lead(models.Model):
    _inherit = 'crm.lead'

    product_subtype_id = fields.Many2one ('veral.product.subtype','Tipo de Máquina')

    # reescribir la funcion onchange_stage_id para que se modifique el valor de res.partner
    # si stage_id nos da una etapa que no se incluya en marketing_campaigne
    # para eso creamos antes el valor no_marketing en crm.case.stage y en partner

    @api.v7
    # def onchange_stage_id(self, cr, uid, ids, stage_id, context=None): 
    def write(self, cr, uid, ids, vals, context=None):       
        partn = self.pool.get('res.partner')
        stage = self.pool.get('crm.case.stage')
        oppor = self.pool.get('crm.lead').browse(cr,uid,ids[0],context=context)
        logger.error('Valor para oppor en onchange_sate_id %s'%oppor[0].name)
        if 'stage_id' in vals:
            stagbrw = stage.browse(cr, uid, vals.get('stage_id'), context=context) 
            if stagbrw:
                logger.error('Valor para stage en onchange_sate_id %s'%stagbrw.name)
                if oppor.partner_id:
                    partsrch = partn.search(cr,uid,[('id','=',oppor.partner_id.id)])
                    logger.error('Valor para partner_id en onchange_sate_id %s'%partsrch[0])
                    if stagbrw.no_marketing:
                        if len(partsrch)>0:
                            partn.write (cr,uid,partsrch[0],{'no_marketing':True})
                    else:
                        #por si el cliente pasa de fase no_marketing a fase marketing
                        if len(partsrch)>0:
                            partn.write (cr,uid,partsrch[0],{'no_marketing':False})

        # super(crm_lead, self).onchange_stage_id(cr, uid, ids, stage_id, context=context)
        return super(crm_lead, self).write(cr, uid, ids, vals, context=context)


class crm_action(models.Model):
    _inherit = 'crm.action'

    product_subtype_id = fields.Many2one (related='lead_id.product_subtype_id',string='Tipo de Máquina', readonly=True, store=True)
