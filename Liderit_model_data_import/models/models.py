from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from openerp import fields,models,api
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging

_logger = logging.getLogger(__name__)


class data_import_model(models.Model):
	_name ="data.import.model"
	
	list_price= fields.Float(String="precio")
	default_code = fields.Char(string ="default code")
	discount = fields.Float (string="descuento")
	standard_price = fields.Float (string="coste")
	


	@api.model
	def update_product(self):
		_logger.error('dentro')
		productos = self.env['data.import.model'].search([])
		for producto in productos:
			try:
				_logger.error('iteracion '+ producto.default_code)
				new_product = self.env['product.template'].search([('default_code','=',producto.default_code)])
				new_product.list_price = producto.list_price
			except:
				_logger.error('fallo '+ producto.default_code)

	@api.model
	def update_product_cost(self):
		_logger.error('dentro')
		productos = self.env['data.import.model'].search([])
		partnerinfo =self.env['pricelist.partnerinfo']
		for producto in productos:
			try:
				_logger.error('iteracion '+ producto.default_code)
				new_product = self.env['product.template'].search([('default_code','=',producto.default_code)])
				new_product.standard_price = producto.standard_price
				productspricelist = partnerinfo.search([('product_tmpl_id','=',new_product.id)])
				for prod in productspricelist:
					prod.discount=producto.discount


			except:
				_logger.error('fallo '+ producto.default_code)
		
