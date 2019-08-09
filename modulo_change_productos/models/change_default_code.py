from openerp import models, api, fields


import logging

_logger = logging.getLogger(__name__)


class product_product (models.Model):
	_inherit =["product.product"]
	_name ="product.product"
	

	@api.model
	def change_default_code(self):
		productos = self.env['product.product'].search([])
		_logger.error('################## Entro en la funcion '+str(productos))
		for producto in productos:
			objeto = self.env['product.product'].search([('id','=',producto.id)])
			_logger.error('################## entro a recorrer los productos '+ objeto.default_code)
			codigo = objeto.default_code
			if objeto.categ_id == 256:
				_logger.error('################## entro en el if de la categoria 256 ')
				if codigo.isnumeric()and len(codigo)<5:
					while len(codigo)<5:
						codigo = "0"+codigo
					objeto.default_code = codigo
			else:
				_logger.error('################## entro en el else de la categoria 256 ')
				if codigo.isnumeric() and len(codigo)<8:
					_logger.error('################## entro a recorrer los productos '+ objeto.default_code)
					_logger.error('################## entro si es numerico '+ codigo)
					while len(codigo)<8:
						codigo = "0"+codigo
					_logger.error('################## el codigo que va a signarse es:  '+ codigo)
					objeto.default_code = codigo