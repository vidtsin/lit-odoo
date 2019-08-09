# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _get_debt(self):
        debt_account = self.env.ref('pos_debt_notebook.debt_account')
        debt_journal = self.env.ref('pos_debt_notebook.debt_journal')

        self._cr.execute(
            """SELECT l.partner_id, SUM(l.debit - l.credit)
            FROM account_move_line l
            WHERE l.account_id = %s AND l.partner_id IN %s
            GROUP BY l.partner_id
            """,
            (debt_account.id, tuple(self.ids)))

        res = {}
        for partner in self:
            res[partner.id] = 0
        for partner_id, val in self._cr.fetchall():
            res[partner_id] += val

        statements = self.env['account.bank.statement'].search(
            [('journal_id', '=', debt_journal.id), ('state', '=', 'open')])
        if statements:

            self._cr.execute(
                """SELECT l.partner_id, SUM(l.amount)
                FROM account_bank_statement_line l
                WHERE l.statement_id IN %s AND l.partner_id IN %s
                GROUP BY l.partner_id
                """,
                (tuple(statements.ids), tuple(self.ids)))
            for partner_id, val in self._cr.fetchall():
                res[partner_id] += val
        for partner in self:
            partner.debt = res[partner.id]

    debt = fields.Float(
        compute='_get_debt', string='Venta Credito TPV', readonly=True,
        digits=dp.get_precision('Account'))


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    debt = fields.Boolean(string='Venta a credtito TPV')


class PosConfig(models.Model):
    _inherit = 'pos.config'

    debt_dummy_product_id = fields.Many2one(
        'product.product', string='Producto de deuda',
        domain=[('available_in_pos', '=', True)], required=True,
      
        help="Producto Maniquí utiliza cuando un cliente paga su deuda sin pedir nuevos productos."
         "Se trata de una solución al hecho que Odoo necesita tener al menos"
         " un producto en la orden de validar la transacción.")
