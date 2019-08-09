from openerp import models, fields, api, exceptions, _
from openerp.osv import osv

from dateutil.relativedelta import relativedelta
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


# para un nuevo campo de aplazamiento de todos los vencimientos de la factura
class account_invoice(models.Model):
    _inherit = 'account.invoice'


    maturity_postpone = fields.Float(string='Postpone dues')
    due_date_beguin = fields.Date(string=_('Initial Due Date'))
    due_lines = fields.One2many(
    	comodel_name='account.move.line', 
    	inverse_name='invoice',
    	domain=[('account_id.type', 'in', ['receivable', 'payable'])]
    	)

    @api.onchange('maturity_postpone')
    def onchange_maturity_postpone(self):
        # almacenamos el cambio de valor entre el aplazamiento nuevo y el anterior
        change = self.maturity_postpone - self._origin.maturity_postpone
        # _logger.error('######## AIKO valor para invoice_id en onchange maturity  %s ####### ->'%self._origin.id)

        move_obj = self.env['account.move.line'].search([('stored_invoice_id','=',self._origin.id),('maturity_residual','>',0.0)])
        _logger.error('######## AIKO valor para move_lines en onchange maturity  %s ####### ->'%move_obj)

        for move in move_obj:
            # _logger.error('######## AIKO valor para move maturity en onchange maturity  %s ####### ->'%move.date_maturity)
            if move.date_maturity:
                date = fields.Date.from_string(move.date_maturity)
                new_date= date + relativedelta(days=+change)
                # _logger.error('######## AIKO valor para nuevo due en onchange maturity  %s ####### ->'%fields.Date.to_string(new_date))
                move.write({'date_maturity': new_date})



    @api.onchange('due_date_beguin')
    def onchange_due_date_beguin(self):
        move_obj = self.env['account.move.line'].search([('stored_invoice_id','=',self._origin.id),('maturity_residual','>',0.0)])
        pay_lines = self.env['payment.line']

        #obtener el menor de los vencimientos
        if move_obj:
            #revisamos no este alguno cobrado
            for move in move_obj:
                if move.reconcile_partial_id or move.reconcile_id:
                    raise Warning(_('You can not change paid dues.'))
                    move_obj =[]
                    break
                #o que alguno pueda estar en una remesa de cobro
                m_in_line = pay_lines.search([('move_line_id','=',move.id),('order_id.state','!=','cancel')])
                if m_in_line:
                    raise Warning(_('You can not change paid dues.'))
                    move_obj =[]
                    break

            if not self._origin.due_date_beguin:
                pterm_list=[]
                for move in move_obj:
                    pterm_list.append(move.date_maturity)
                pterm_list.sort()
                # _logger.error('######## AIKO valor para pterm_list en onchange date_beguin  %s ####### ->'%pterm_list)
                date_maturity = pterm_list[0]
                if date_maturity and self.due_date_beguin:
                    date_maturity = fields.Date.from_string(date_maturity)
                    change = fields.Date.from_string(self.due_date_beguin) - date_maturity
            else:
                change = fields.Date.from_string(self.due_date_beguin) - fields.Date.from_string(self._origin.due_date_beguin)
            # _logger.error('######## AIKO valor para change en onchange date_beguin  %s ####### ->'%change)

            for move in move_obj:
                if move.date_maturity:
                    date = fields.Date.from_string(move.date_maturity)
                    #new_date= date + relativedelta(days=+change)
                    new_date = date + change
                    # _logger.error('######## AIKO valor para nuevo due en onchange maturity  %s ####### ->'%fields.Date.to_string(new_date))
                    move.write({'date_maturity': new_date})
