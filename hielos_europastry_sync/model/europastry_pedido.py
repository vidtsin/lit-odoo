#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#################################################################################
from openerp import api,fields,models
from openerp.tools.translate import _
from datetime import datetime,timedelta
import base64
import paramiko
import csv
import pysftp
from ftplib import FTP
import urllib 
import glob, os, sys, stat, shutil
import unicodedata
import logging
_logger	 = logging.getLogger(__name__)


class europastry_pedido(models.Model):
	_name = "europastry.pedido"

	cod_dist = fields.Integer(string=_('Codigo Distribuidor'))
	n_pedido_eurp = fields.Char (string = _('Nº Pedido Europastry'))
	tip_ped =fields.Char(string = _('Tipo de pedido'))
	cod_cli = fields.Integer(string = _('Codigo Cliente'))	
	nom_cli = fields.Char (string = _('Nombre Cliente'))
	raz_social = fields.Char (string = _('Razon Social'))
	cp = fields.Integer (string = _('Codigo Postal'))
	provincia = fields.Char (string = _('Provincia'))
	num_ped_cli = fields.Char (string= _('Pedido de cliente'))
	fecha_intro = fields.Char(string = _('Fecha Introduccion Pedido'))
	fecha_entrega_t =fields.Char(string = _('Fecha Entrega Teorica'))
	obser =fields.Char (string = _('Observaciones'))
	cod_articulo = fields.Char (string = _('Codigo Articulo'))
	cod_ean_articulo = fields.Char (string = _('Codigo EAN Articulo'))
	cantidad = fields.Integer (string = _('Cantidad'))
	unidad_med = fields.Char (string = _('Unidad de Medida'))
	obsequio = fields.Char (string = _('Obsequio'))
	promo = fields.Char (string = _('Codigo Promocion'))
	excepcion = fields.Char(string=_('Excepciones'))
	procesada = fields.Boolean(string = _('Procesado'))
	fichero_import = fields.Char(string = _('Fichero Importacion'))

	
	@api.model
	def import_orders_europ(self):
		ftp_europastry = self.env['ir.config_parameter'].sudo().get_param('ftp_europastry')
		_logger.error('ftp europastry '+ ftp_europastry)
		ftp_user=self.env['ir.config_parameter'].sudo().get_param('ftp_user')
		ftp_pass=self.env['ir.config_parameter'].sudo().get_param('ftp_pass')
		ftp_path=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		ftp_dist_europ=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		cnopts = pysftp.CnOpts()
		local_path='/var/ftp/EUROPASTRY/Pedidos/'
		ftp_path=ftp_path+'/Pedidos/'
		_logger.error('ftp path '+ftp_path)
		
		
		cnopts.hostkeys = None

		

		# Make connection to sFTP
		with pysftp.Connection(ftp_europastry,
						username=ftp_user,
						password=ftp_pass,
						cnopts=cnopts,
						) as sftp:
			ficheros=sftp.listdir(ftp_path) #ficheros=sftp.listdir('/var/ftp/EUROPASTRY')
			for file in ficheros:
				_logger.error('file '+file)
				pre=file[:14]
				_logger.error('pre '+pre)
				ext=file[-4:]
				_logger.error('ext '+ext)
				
				if (str(pre)=='436381_pedidos') and (str(ext) =='.txt' or str(ext) =='.TXT'):
					sftp.get(ftp_path+file,local_path+file)
		
					source = ftp_path+file
					destino =ftp_path+'Tratados/'+file
					local_source=local_path+'/'+file
					local_dest=local_path+'Tratados/'+file
					_logger.error('europastry '+str(datetime.now()))
					try:
						with open(local_source) as csv_file:
							csv_reader = csv.reader(csv_file, delimiter=';')
							if csv_file:
								line_count = 0
								for row in csv_reader:
									fila=str(row)								
									fila=fila.split(";")
									line_count += 1
									cp = 0
									cant=0
									bruto=0
									neto=0
									if row[6]:
										cp = int(row[6])
									if row[14]:
										cant = int(row[14])

									self.create({
										'cod_dist' : int(row[0]),
										'n_pedido_eurp' : row[1],
										'tip_ped' : row[2],
										'cod_cli' : int(row[3]),
										'nom_cli' : row[4],
										'raz_social' : row[5],
										'cp' : cp,
										'provincia' : row[7],
										'num_ped_cli' : row[8],
										'fecha_intro' : row[9],
										'fecha_entrega_t' : row[10],
										'obser' : row[11],	
										'cod_articulo' : row[12],
										'cod_ean_articulo' : row[13],
										'cantidad' : cant,
										'unidad_med' : row[15],
										'obsequio' : row[16],
										'promo' : row[17], 
										'procesada' : False,
										'fichero_import' : source
									})
					except:
						_logger.error('file not exist')

					shutil.move(local_source, local_dest)
					sftp.rename(source,destino)
		
		
		return

	


class SaleOrder(models.Model):

	_inherit = 'sale.order'

	is_europastry = fields.Boolean(string=_('Europastry'))
	europastry_pick = fields.Char(string = _('Europastry Picking'))
	europastry_order = fields.Char(string=_('Europastry order'))
	fecha_intro = fields.Char(string = _('Fecha Introduccion Pedido'))
	fecha_entrega_t = fields.Char(string = _('Fecha Entrega Teorica'))
	tip_ped = fields.Char(string = _('Tipo de pedido'))
	num_ped_cli = fields.Char (string= _('Pedido de cliente'))
	europ_obseq = fields.Char(string=_('Obsequio'))
	promo = fields.Char (string = _('Codigo Promocion'))
	motivo_no_ent=fields.Char (string = _('Motivo No Entregado'))
	_vals={}
	_lines={}

	# Methods
	@api.model
	def create_orders_europ(self):
		
		#recupera todas las lineas sin procesar
		lines=self.env['europastry.pedido'].search([('procesada','=',False)])
		_logger.error('inicia cron '+ str(lines))
		orders=[]
		#itera las lineas
		for line in lines:
			
			saleman=self.env['res.users'].search([('login','=','europastry')])
			if not saleman:
				saleman=self.env['res.users'].search([('login','=','admin')])
			line_exception=""
			cod_cli=str(line.cod_cli)
			cod_cli='4300'+cod_cli
			_logger.error(cod_cli)
			cli_europ = self.env['res.partner'].search([('ref','=',cod_cli)])
			_logger.error('cli'+str(cli_europ))
			#si no encuentra el cliente ande mensaje a la excepcion de la linea
			if not cli_europ:
				line_exception=line_exception+'-- No encuentra cliente '+str(line.cod_cli)+ ' - '
			#intenta cargar la orden de europastry por si ya esta creada	
			order_europ=self.env['sale.order'].search([('europastry_order','=',line.n_pedido_eurp)])

			#_logger.error('order '+str(order_europ))
			#_logger.error('line prod  '+str(line.cod_articulo))
			
			product = self.env['product.product'].search([('default_code','=',str(line.cod_articulo))])
			#si no encuentra el producto anade a la excepcion
			if not product:
				line_exception=line_exception+'-- No encuentra producto '+str(line.cod_articulo)+ ' - '
			#_logger.error('prod'+str(product))
			unidad_uom = self.env['product.uom'].search([('name','=',line.unidad_med)])
			# si no encuentra unidad de medida lo anade a la excepcion
			if not unidad_uom:
				line_exception=line_exception+'-- No encuentra unidad de medida'+str(line.unidad_med)+ ' - '
			#_logger.error('unidad de medida '+str(line.unidad_med))
			#si encunetra una orden con ese num de pedido de europastry, el cliente, el producto y la unidad de medida,
			
			if order_europ:
				if cli_europ and product and unidad_uom:
					#crea la linea en el pedido encontrado.
					#_logger.error('encuentra orden')
					#_logger.error('order '+str(order_europ.id))
					
					taxes_ids=[]
					for tax in product.taxes_id:
						#_logger.error('product tax id ' + str(tax))
						taxes_ids.append(tax.id)
					self._lines={}

					self._lines={
							'product_id' : product.id,
							'product_uos_qty': line.cantidad,
							'product_uom': unidad_uom.id,
							#'sequence': 20,
							'price_unit': product.list_price,
							'product_uom_qty': line.cantidad,
							'product_uos':unidad_uom.id,
							'company_id': 1,
							'name': product.name,
							#'delay': 0,
							#'state': 'confirmed',
							'order_partner_id': cli_europ.id,
							'order_id': order_europ.id,
							'discount': 0,
							'salesman_id': saleman.id,
							'tax_id': [(6, 0, taxes_ids)],
							'product_template': product.id,							
							}

					
					self.add_to_offer(self)
					#cambia la linea a procesada
					line.procesada=True
					#_logger.error('creada linea')

			else:
				#si no encuentra pedido con ese numero, lo crea
				_logger.error('no encuentra orden')
				self._vals={
						'partner_id' : cli_europ.id,
						'is_europastry' : True,
						'europastry_order' :line.n_pedido_eurp or "",
						'fecha_entrega_t' : line.fecha_entrega_t or "",
						'fecha_intro' : line.fecha_intro or "",
						'tip_ped' :line.tip_ped or "",
						'num_ped_cli' : line.num_ped_cli or "",
						'note' : line.obser or "",
						}
				
				if cli_europ:
					_logger.error('###########################  crea orden')
					self.create_order_europ(self)

				#_logger.error('crea orden')
				order_europ=self.env['sale.order'].search([('europastry_order','=',line.n_pedido_eurp)])
				#si no encuentra el pedido recien creado lo suma a la excepcion
				if not order_europ:
					line_exception=line_exception+'-- orden no creada correctamente '+str(line.n_pedido_eurp)+ ' - '
				#_logger.error('order '+str(order_europ.id))
				#_logger.error('product tax id ' + product.taxes_id.id)
				#si encunetra una orden con ese num de pedido de europastry, el cliente, el producto y la unidad de medida,
				#crea la linea en el pedido encontrado.
				if order_europ and cli_europ and product and unidad_uom:
					taxes_ids=[]
					for tax in product.taxes_id:
						#_logger.error('product tax id ' + str(tax))
						taxes_ids.append(tax.id)
					self._lines={}
					self._lines={
							'product_id' : product.id,
							'product_uos_qty': line.cantidad,
							'product_uom': unidad_uom.id,
							#'sequence': 20,
							'price_unit': product.list_price,
							'product_uom_qty': line.cantidad,
							'product_uos':unidad_uom.id,
							'company_id': 1,
							'name': product.name,
							#'delay': 0,
							#'state': 'confirmed',
							'order_partner_id': cli_europ.id,
							'order_id': order_europ.id,
							'discount': 0,
							'salesman_id': saleman.id,
							'tax_id': [(6, 0, taxes_ids)],
							'product_template': product.id,
							}

					self.add_to_offer(self)
					#cambia la linea a procesado
					line.procesada=True
					#_logger.error('creada linea')
			#almacena las excepciones
			if order_europ not in orders:
				orders.append(order_europ)
			line.excepcion=line_exception

			

		self.confirmsale(orders)
				
		

	@api.model
	@api.returns('sale.order')
	def create_order_europ(self,vals):
		try:
			_logger.error('crea orden'+str(self._vals))
			IrSeq = self.env['ir.sequence']
						
			self._vals['name'] = IrSeq.next_by_code('europastry.pedido')
			
			return super(SaleOrder, self).create(self._vals)
		except:
			return

	@api.model
	#@api.returns('sale.order.line')
	def add_to_offer(self,lines):
		try:

			_logger.error('crea linea'+str(self._lines))
			line_env = self.env['sale.order.line']				
			new_line = line_env.create(self._lines)
		except:
			_logger.error('fallo en linea '+str(self._lines))

	@api.multi
	def confirmsale(self,orders):
		for order in orders:
			order.action_button_confirm()
						
			pick=self.env['stock.picking'].search([('origin','=',order.name)])
			for p in pick:

				sec=self.env['ir.sequence']
				sec_alb=sec.search([('name','=',"Central Secuencia entregas")])
				
				p.name=sec.next_by_code('europastry.picking')
				for seq in sec_alb:
					_logger.error("########################### sequencia albaran antes -- "+ str(seq.number_next_actual))
					seq.number_next_actual=seq.number_next_actual-1
					_logger.error("########################### sequencia albaran despues -- "+ str(seq.number_next_actual))
				p.is_europastry=True
				p.europastry_pick=order.europastry_pick
				p.europastry_order=order.europastry_order
				p.fecha_intro=order.fecha_intro
				p.fecha_entrega_t=order.fecha_entrega_t
				p.tip_ped=order.tip_ped
				p.num_ped_cli=order.num_ped_cli
				p.europ_obseq=order.europ_obseq
				p.promo=order.promo
				p.motivo_no_ent=order.motivo_no_ent
				p.date_min=order.fecha_entrega_t


		#if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
		#	self.action_done()
		

class product_template(models.Model):
    _inherit = "product.template"

    is_europastry = fields.Boolean(string = _('Europastry product'))

