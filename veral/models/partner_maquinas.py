# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
from openerp.osv import osv, fields
from openerp import tools
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

#creamos una clase para tener en una vista los datos de maquinas por clientes
class veral_partner_maquinas(osv.osv):
    _name = "veral.partner.maquinas"
    #auto False para que no genere una tabla, porque es una vista
    _auto = False
    _columns = {
        'name': fields.char('Cliente', readonly=True),
        'phone': fields.char('Teléfono', readonly=True),
        'email': fields.char('Email', readonly=True),
        'fecha_alta': fields.char('Año Alta', readonly=True),
        'no_marketing': fields.float('No activo para marketing',readonly=True),
        'maquina': fields.char('Máquina', readonly=True),
        'date': fields.char('Año', readonly=True),
        'notas': fields.text('Notas', readonly=True),
        'tipo': fields.char('Tipo de máquina', readonly=True),
        'clase':fields.char('Clase de máquina', readonly=True),
        'estado': fields.char('Estado', readonly=True),
        'subtype_id': fields.float('Subtipo',readonly=True),
    }
    _order = 'name, date, maquina'


    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'veral_partner_maquinas')
        cr.execute("""
            CREATE OR REPLACE VIEW veral_partner_maquinas AS (
select 
            prod.id, 
            p.name, 
            p.phone,
            p.email,
            p.fecha_alta,
            CASE WHEN p.no_marketing = 'True' THEN 1
            ELSE 0
            END as no_marketing,
            prod.name as maquina, 
            prod.date,
            prod.notas,
            ptype.name as tipo, 
            sub.name as clase, 
            sub.estado,
            sub.id as subtype_id

from res_partner p join veral_partner_product prod
            on prod.partner_id = p.id left join veral_product_subtype sub
            on prod.subproduct_id = sub.id left join veral_product_type ptype
            on sub.product_type = ptype.id
where p.customer and prod.baja is null and p.name <> 'Public user'
            )
        """)


