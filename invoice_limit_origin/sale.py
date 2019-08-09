# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import ustr

import logging
_logger = logging.getLogger(__name__)

class sale_make_invoice(osv.osv_memory):
    _inherit= 'sale.make.invoice'

    def make_invoices(self, cr, uid, ids, context=None):

        invoice_obj = self.pool.get('account.invoice')

        resultado = super(sale_make_invoice, self).make_invoices(cr, uid, ids, context=context)
        #_logger.error('##### AIKO ###### Invoice Limit Origin. Valor de resultado %s'%resultado)

        if resultado:
            search_condition = [('name','!=',False)]
            invoice_obj_src = invoice_obj.search(cr, uid, search_condition)
            for inv in invoice_obj_src:
                inv_brw = invoice_obj.browse(cr,uid,inv)
                if len(ustr(inv_brw.name))>150:
                    #vamos a tomar los 150 primeros caracteres solamente para que no desborde la pantalla
                    ori_limit = ustr(inv_brw.origin)[:150]
                    name_limit = ustr(inv_brw.name)[:150]
                    ref_limit = ustr(inv_brw.reference)[:150]
                    invoice_obj.write (cr, uid, inv, {'origin': ori_limit,'name': name_limit, 'reference':ref_limit})

        return resultado