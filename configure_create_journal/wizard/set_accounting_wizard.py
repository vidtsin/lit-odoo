# coding: utf-8
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: Jorge Angel Naranjo(jorge_nr@vauxoo.com)
############################################################################
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
import logging 
_logger = logging.getLogger(__name__)
class ConfigureCreateJournal(osv.osv_memory):
    _name = 'configure.create.journal'

    _columns = {
        'warehouse_id': fields.many2one('stock.warehouse', 'Almacen')
    }

    def configure_journal(self, cr, uid, ids, context=None):

        sequence_obj = self.pool.get('ir.sequence')
        journal_obj = self.pool.get('account.journal')
        
        warehouse_obj = self.pool.get('stock.warehouse')
  
        form = self.browse(cr, uid, ids[0])
       

      
        warehouse_ids = warehouse_obj.search(cr, uid, [])
       
        for warehouse_id in warehouse_ids :
            wa=warehouse_obj.browse(cr, uid, warehouse_id ,context=context)
#   Diario de Ventas 
            values = {}
            values['name'] = wa.code + ' Facturas Diario de Ventas'          
            values['company_id'] = wa.company_id.id
            values['prefix'] = wa.code + 'VEN/%(year)s/' 
            values['padding'] = 4
            values['number_increment'] = 1
            values['number_next_actual'] = 1
            values['implementation'] = 'no_gap'
            values['active'] = True
            contador_facturas = sequence_obj.create(cr,uid,values,context=None)
            
            values = {}
            values['name'] = wa.code + ' Asientos Diario de Ventas'
            values['company_id'] = wa.company_id.id
            values['prefix'] = wa.code + 'A_VEN/%(year)s/' 
            values['padding'] = 4
            values['number_increment'] = 1
            values['number_next_actual'] = 1
            values['implementation'] = 'no_gap'
            values['active'] = True
#             contador_asientos = sequence_obj.create(cr,uid,values,context=None)

            values = {}
            values['name'] = wa.code + ' Diario de Ventas'
            
            codigo4= wa.code[0:4]
            codigo1= 'V'
            
            values['code'] = codigo4 + codigo1
            values['type'] = 'sale'
            values['company_id'] = wa.company_id.id
#             values['sequence_id'] = contador_asientos
            values['invoice_sequence_id'] = contador_facturas
            values['entry_posted'] = True
            values['update_posted'] = True
            
            journal = journal_obj.create(cr,uid,values,context=None)
#  Diario de Abono de Ventas 
            values = {}
            values['name'] = wa.code + ' Facturas Rectificativas Diario de Abono Ventas'          
            values['company_id'] = wa.company_id.id
            values['prefix'] = wa.code + 'AVEN/%(year)s/' 
            values['padding'] = 4
            values['number_increment'] = 1
            values['number_next_actual'] = 1
            values['implementation'] = 'no_gap'
            values['active'] = True
            contador_facturas = sequence_obj.create(cr,uid,values,context=None)
            
            values = {}
            values['name'] = wa.code + ' Asientos Facturas Rectificativas Diario de Abono Ventas'
            values['company_id'] = wa.company_id.id
            values['prefix'] = wa.code + 'A_AVEN/%(year)s/' 
            values['padding'] = 4
            values['number_increment'] = 1
            values['number_next_actual'] = 1
            values['implementation'] = 'no_gap'
            values['active'] = True
#             contador_asientos = sequence_obj.create(cr,uid,values,context=None)

            values = {}
            values['name'] = wa.code + ' Diario de Abono de Ventas'
            
            codigo4= wa.code[0:4]
            codigo1= 'A'
            
            values['code'] = codigo4 + codigo1
            values['type'] = 'sale_refund'
            values['company_id'] = wa.company_id.id
#             values['sequence_id'] = contador_asientos
            values['invoice_sequence_id'] = contador_facturas
            values['entry_posted'] = True
            values['update_posted'] = True
            journal = journal_obj.create(cr,uid,values,context=None)
 
        return False
