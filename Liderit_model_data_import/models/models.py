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
		
class import_data_customer_price(models.Model):
	_name ="import.data.customer.price"
	
	list_price= fields.Float(String="precio")
	default_code = fields.Char(string ="default code")
	discount = fields.Float (string="descuento")
	tipo = fields.Char (string="Tipo")
	ref = fields.Char (string ="referencia cliente")

	@api.model
	def insert_precios_productos_cliente(self):
		registros = self.env['import.data.customer.price'].search([])

		_logger.error('dentro funcion para insertar precios por cliente')

		ref_not_in = []

		for linea in registros:
			try: 
				_logger.error('entro a recorrer los registros del modelo')
				product_tmpl = self.env['product.template'].search([('default_code','=',linea.default_code)])
				cliente = self.env['res.partner'].search([('ref','=',linea.ref)])

				tmpl_id = product_tmpl.id
				partner_id = cliente.id

				if linea.tipo =='customer' and partner_id != 0:
					_logger.error('entro al if que hace el Create')

					self.env['product.supplierinfo'].create({
						'product_tmpl_id':tmpl_id,
						'name':partner_id,
						'type':linea.tipo,
						})

					suppinfo = self.env['product.supplierinfo'].search([('name','=',partner_id),('product_tmpl_id','=',tmpl_id),('type','=',linea.tipo)])

					suppinfo_id = suppinfo.id
					cantidad = 0.0


					self.env['pricelist.partnerinfo'].create({
						'product_tmpl_id':tmpl_id,
						'partner': partner_id,
						'type':linea.tipo,
						'discount':linea.discount,
						'price':linea.list_price,
						'suppinfo_id':suppinfo_id,
						'min_quantity':cantidad,
						})
				else:
					_logger.error('referencia de cliente que no existe '+ linea.ref)

					if linea.ref not in ref_not_in:
						ref_not_in.append(linea.ref)

			except:
				_logger.error('fallo '+ linea.ref)

		_logger.error('todas las referencias de cliente que no estaban '+ str(ref_not_in))



