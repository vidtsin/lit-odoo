# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountBankingMandate(models.Model):
    """SEPA Direct Debit Mandate"""
    _inherit = 'account.banking.mandate'

    scheme = fields.Selection([('CORE', 'Basic (CORE)'),
                               ('COR1', 'Basic (COR1)'),
                               ('B2B', 'Enterprise (B2B)')],
                              string='Scheme', default="CORE")
