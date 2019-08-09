# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _
from datetime import datetime,timedelta
import logging
_logger	 = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = "res.partner"

    is_europastry = fields.Boolean(string = _('Europastry Client'))
    zona_comercial = fields.Char(string = _('Zona Comercial'))
    europ_potencial = fields.Char(string = _('Potencial'))
    europ_cuota = fields.Char(string = _('Cuota'))
    europ_competencia = fields.Char(string = _('Competencia'))
    


