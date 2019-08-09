#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#################################################################################
from openerp import api,fields,models
from openerp.tools.translate import _
from datetime import datetime,timedelta
import csv
import glob, os, sys, stat, shutil
import unicodedata
import base64
import paramiko
import pysftp
from ftplib import FTP
import urllib 
import logging
_logger	 = logging.getLogger(__name__)


class StockPicking(models.Model):

	_inherit = 'stock.picking'

	is_europastry = fields.Boolean(string=_('Europastry'))
	europastry_pick = fields.Char(string = _('Europastry Picking'))
	europastry_order = fields.Char(string=_('Europastry order'))
	europ_identicket = fields.Char(string=_('Identicket'))
	fecha_intro = fields.Char(string = _('Fecha Introduccion Pedido'))
	fecha_entrega_t =fields.Char(string = _('Fecha Entrega Teorica'))
	tip_ped =fields.Char(string = _('Tipo de pedido'))
	num_ped_cli = fields.Char (string= _('Pedido de cliente'))
	europ_obseq = fields.Char(string=_('Obsequio'))
	motivo_no_ent = fields.Char (string = _('Motivo No Entregado'))
	promo = fields.Char (string = _('Codigo Promocion'))
	#order_origin= fields.Char(string=_('or'),compute='_update_europastry_fields')

	
		


class europastry_sinc(models.Model):
	_name = "europastry.sync"

	cod_dist = fields.Integer(string=_('Codigo Distribuidor'))
	cod_cli = fields.Integer(string = _('Codigo Cliente'))
	cli_euro = fields.Char(string = _('Cliente Europastry'))
	num_alb =fields.Char(string = _('Numero de Albaran'))
	fecha_intro = fields.Char(string = _('Fecha Introduccion Pedido'))
	fecha_entrega_t =fields.Char(string = _('Fecha Entrega Teorica'))
	fecha_alb = fields.Char(string = _('Fecha Albaran'))
	num_fact = fields.Char(string =_('Numero de Factura'))
	fecha_fact =fields.Char(string = _('Fecha Factura'))
	nom_cli = fields.Char (string = _('Nombre Cliente'))
	raz_social = fields.Char (string = _('Razon Social'))
	nif_cif = fields.Char (string = _('NIF CIF CIE'))	
	direccion = fields.Char (string = _('Direccion'))
	poblacion = fields.Char (string = _('Poblacion'))
	provincia = fields.Char (string = _('Provincia'))
	cp = fields.Integer (string = _('Codigo Postal'))
	telef = fields.Char (string = _('Telefono'))
	fax = fields.Char (string = _('Fax'))
	zona_com = fields.Char (string = _('Zona Comercial'))
	fecha_alta = fields.Char (string = _('Fecha Alta'))
	num_orden_comp =fields.Char (string = _('Numero Orden Compra'))
	num_identicket = fields.Char (string = _('Numero Identicket'))
	cod_articulo = fields.Char (string = _('Codigo Articulo'))
	fab_artic = fields.Char (string = _('Fabricante del Articulo'))
	cantidad = fields.Integer (string = _('Cantidad'))
	unidad_med = fields.Char (string = _('Unidad de Medida'))
	obsequio = fields.Char (string = _('Obsequio'))
	lote = fields.Char (string = _('Lote'))
	imp_bruto = fields.Float (string = _('Importe Bruto'))
	imp_neto = fields.Float (string = _('Importe Neto'))
	divisa = fields.Char (string = _('Divisa'))
	co_promo = fields.Char (string = _('Codigo Promoción'))
	obser =fields.Char (string = _('Observaciones'))
	potencial = fields.Char (string = _('Potencial'))
	cuota = fields.Char (string = _('Cuota'))
	competencia = fields.Char (string = _('Competencia'))
	n_pedido_eurp = fields.Char (string = _('Nº Pedido Europastry'))
	motivo_no_ent = fields.Char (string = _('Motivo No Entregado'))
	fichero_import = fields.Char(string = _('Fichero Importacion'))
	excepcion = fields.Char(string=_('Excepciones'))
	procesada = fields.Boolean(string = _('Procesado'))


	@api.model
	def create_entregas_europ(self):
		now = datetime.now()
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		_logger.error('inicia create_enmtregas_europ '+str(datetime.now()))
		
		
		date45= now-timedelta(days=45)
		date45 =date45.strftime("%Y-%m-%d %I:%M:%S")
		_logger.error('45 dias  '+str(date45))
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		pickings=self.env['stock.picking'].search([('state','!=','cancel'),'|',('date_done','>',date45),('date_done','=',False)])
		_logger.error('Albaranes '+str(pickings))
		for picking in pickings:
			#lines=self.env['stock.move'].search([('picking_id','=',picking.id)])
			#order=self.env['sale.order'].search([('name','=',picking.origin)])
			
			for line in picking.move_lines:
				
				nombre_categ="EP-PRODUCTOS EUROPASTRY"
				product_categ=line.product_id.categ_id.name
				_logger.error('es europastry' + product_categ.strip()+' == '+nombre_categ.strip()+' es ')
				#_logger.error(product_categ.strip() == nombre_categ.strip())
				if (product_categ.strip() == nombre_categ.strip()):
					#_logger.error('si' + line.product_id.name)
					lotes=""
					for lote in line.lot_ids:
						lotes=lotes+", "+lote.name

					same_line=self.search([('procesada','=',False),('lote','=',lotes),('cod_cli','=',int(picking.partner_id.ref[4:])),('num_alb','=',str(picking.europastry_pick)),('cod_articulo','=',str(line.product_id.default_code)),('unidad_med','=',str(line.product_uom.name))])
					if same_line:
						
						cantidad=same_line.cantidad+int(line.product_uos_qty)
						#_logger.error('linea encontrada cantidad'+str(cantidad)+' linea '+ str(same_line))
						same_line.cantidad=cantidad
						same_line.imp_neto= line.product_id.list_price*cantidad

					else:
						num_fact=""
						fecha_fact=""
						for invoice in picking.sale_id.invoice_ids:
							
							if invoice.date_invoice and invoice.number:
								num_fact=invoice.number
								fecha_fact=datetime.strptime(invoice.date_invoice, '%Y-%m-%d')						
								fecha_fact =fecha_fact.strftime("%d/%m/%Y")
							
						#_logger.error('############################ factura '+ str(fecha_fact))
						cantidad=int(line.product_uos_qty)
						fecha_albaran=""
						if picking.date:
							fecha_albaran=datetime.strptime(picking.date, '%Y-%m-%d %H:%M:%S')						
							fecha_albaran =fecha_albaran.strftime("%d/%m/%Y")
						#_logger.error('############################ factura '+ str(fecha_albaran))

						fecha_alta=""
						if picking.partner_id.create_date:
							fecha_alta=datetime.strptime(picking.partner_id.create_date, '%Y-%m-%d %H:%M:%S')						
							fecha_alta =fecha_alta.strftime("%d/%m/%Y")

						fecha_min=""
						if picking.min_date:
							fecha_min=datetime.strptime(picking.min_date, '%Y-%m-%d %H:%M:%S')						
							fecha_min =fecha_min.strftime("%d/%m/%Y")

						#_logger.error('############################ fecha alta '+ str(fecha_alta))
						#_logger.error('############################ pedido eurpastry '+ str(picking.europastry_order))
						if picking.partner_id.is_europastry:
							cli_euro="SI"
							cli_nombre=""
							cli_razsoc=""
							cli_nif=""
							cli_dir=""
							cli_pob=""
							cli_prov=""
							cli_cp=""
							cli_telef=""
							cli_fax=""
							cli_zona=""
						else:
							cli_euro="NO"
							cli_nombre=picking.partner_id.name.strip() or ""
							cli_nombre=cli_nombre.decode('unicode-escape')
							cli_razsoc=picking.partner_id.comercial.strip() or ""
							cli_razsoc=cli_razsoc.decode('unicode-escape')
							cli_nif=picking.partner_id.vat.strip() or ""

							cli_dir=picking.partner_id.street.strip() or ""
							#_logger.error(cli_dir)
							cli_dir=cli_dir.decode('unicode-escape')
							cli_pob=picking.partner_id.city.strip() or ""
							cli_prov=""
							cli_cp=""
							cli_telef=picking.partner_id.phone or ""
							cli_fax=picking.partner_id.fax or ""
							cli_zona=""
						
						self.create({
							'cod_dist' : 436381,
							'cod_cli' : int(picking.partner_id.ref[4:]),
							'cli_euro' : cli_euro,
							'num_alb' :str(picking.name or ""),
							'fecha_intro' : picking.fecha_intro or "",
							'fecha_entrega_t' : fecha_min,
							'fecha_alb' : fecha_albaran,
							'num_fact' : num_fact,
							'fecha_fact': fecha_fact,
							'nom_cli' : cli_nombre,
							'raz_social' :cli_razsoc,
							'nif_cif' : cli_nif,	
							'direccion' : cli_dir,
							'poblacion' : cli_pob,
							'provincia': cli_prov,
							'cp': cli_cp,
							'telef' : cli_telef,
							'fax' : cli_fax,
							'zona_com' : cli_zona,
							'fecha_alta' : fecha_alta,
							'num_orden_comp' : picking.num_ped_cli or "",
							'num_identicket' :picking.europ_identicket or "",
							'cod_articulo' : str(line.product_id.default_code or ""),
							'fab_artic' : "SI",				
							'cantidad' : cantidad or "",
							'unidad_med' : str(line.product_uom.name or ""),					
							'obsequio' : picking.europ_obseq or "",
							'lote' : lotes or "",
							'imp_bruto' : line.product_id.list_price or "",
							'imp_neto' : line.product_id.list_price*cantidad,
							'divisa' : "EUR",
							'co_promo' : picking.promo or "",
							'obser' : picking.sale_id.note or "",
							'potencial' :picking.partner_id.europ_potencial or "",
							'cuota' : picking.partner_id.europ_cuota,
							'competencia' : picking.partner_id.europ_competencia,
							'n_pedido_eurp' : picking.europastry_order or "",
							'motivo_no_ent' : picking.motivo_no_ent or "",					
						})
		

		return

	
	@api.model
	def export_entregas_europ(self):
		now = datetime.now()
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		_logger.error('inicia export_orders_europ '+str(datetime.now()))
		f = open('/var/ftp/EUROPASTRY/436381_'+date+'.txt', 'wt')

		try:
			lines=self.env['europastry.sync'].search([('procesada','=',False)])
			writer = csv.writer(f,delimiter=';')
			
			for line in lines:
				writer.writerow(( 
					line.cod_dist,
					line.cod_cli,
					line.cli_euro,
					line.num_alb,
					line.fecha_intro,
					line.fecha_entrega_t,
					line.fecha_alb,
					line.num_fact,
					line.fecha_fact,
					line.nom_cli,
					line.raz_social,
					line.nif_cif,	
					line.direccion,
					line.poblacion,
					line.provincia,
					line.cp,
					line.telef,
					line.fax,
					line.zona_com,
					line.fecha_alta,
					line.num_orden_comp,
					line.num_identicket,
					line.cod_articulo,
					line.fab_artic,
					line.cantidad,
					line.unidad_med,
					line.obsequio,
					line.lote,
					line.imp_bruto,
					line.imp_neto,
					line.divisa,
					line.co_promo,
					line.obser,
					line.potencial,
					line.cuota,
					line.competencia,
					line.n_pedido_eurp,
					line.motivo_no_ent))
				line.procesada=True
		finally:
			f.close()

		ftp_europastry = self.env['ir.config_parameter'].sudo().get_param('ftp_europastry')
		_logger.error('ftp europastry '+ ftp_europastry)
		ftp_user=self.env['ir.config_parameter'].sudo().get_param('ftp_user')
		ftp_pass=self.env['ir.config_parameter'].sudo().get_param('ftp_pass')
		ftp_path=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		ftp_dist_europ=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		cnopts = pysftp.CnOpts()
		local_path='/var/ftp/EUROPASTRY/436381_'+date+'.txt'
		destino=ftp_path+'/436381_'+date+'.txt'
		
		cnopts.hostkeys = None

		

		# Make connection to sFTP
		with pysftp.Connection(ftp_europastry,
						username=ftp_user,
						password=ftp_pass,
						cnopts=cnopts,
						) as sftp:
			sftp.put(local_path,destino)


		
		return

	


class europastry_seguimiento(models.Model):

	_name = "europastry.seguimiento"

	cod_dist = fields.Integer(string=_('Codigo Distribuidor'))
	n_pedido_eurp = fields.Char (string = _('Nº Pedido Europastry'))
	tip_ped =fields.Char(string = _('Tipo de pedido'))
	cod_cli = fields.Integer(string = _('Codigo Cliente'))
	fecha_entrega_s = fields.Char(string = _('Fecha Entrega Solicitada'))
	fecha_entrega_t =fields.Char(string = _('Fecha Entrega Teorica'))
	fecha_entrega_r =fields.Char(string = _('Fecha Entrega Real'))	
	cod_articulo = fields.Char (string = _('Codigo Articulo'))
	cantidad = fields.Integer (string = _('Cantidad'))
	unidad_med = fields.Char (string = _('Unidad de Medida'))
	cancelada = fields.Char (string = _('Cancelada'))
	obser =fields.Char (string = _('Observaciones'))
	procesada = fields.Boolean(string = _('Procesado'))


	@api.model
	def export_seguimiento_europ(self):
		_logger.error('inicia export_seguimiento_europ '+str(datetime.now()))
		now = datetime.now()
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		f = open('/var/ftp/EUROPASTRY/Seguimiento/436381_seguimiento_'+date+'.txt', 'wt')
		try:
			lines=self.env['europastry.seguimiento'].search([('procesada','=',False)])
			writer = csv.writer(f,delimiter=';')
			#writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
			for line in lines:
				writer.writerow(( 
					line.cod_dist,
					line.n_pedido_eurp,
					line.tip_ped,
					line.cod_cli,
					line.fecha_entrega_s,
					line.fecha_entrega_t,
					line.fecha_entrega_r,
					line.cod_articulo,
					line.cantidad,
					line.unidad_med,
					line.cancelada,
					line.obser))
				line.procesada=True

		finally:
			f.close()

		ftp_europastry = self.env['ir.config_parameter'].sudo().get_param('ftp_europastry')
		_logger.error('ftp europastry '+ ftp_europastry)
		ftp_user=self.env['ir.config_parameter'].sudo().get_param('ftp_user')
		ftp_pass=self.env['ir.config_parameter'].sudo().get_param('ftp_pass')
		ftp_path=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		ftp_dist_europ=self.env['ir.config_parameter'].sudo().get_param('ftp_path')
		cnopts = pysftp.CnOpts()

		local_path='/var/ftp/EUROPASTRY/Seguimiento/436381_seguimiento_'+date+'.txt'
		
		destino=ftp_path+'/Seguimiento/436381_seguimiento_'+date+'.txt'
		
		
		cnopts.hostkeys = None

		

		# Make connection to sFTP
		with pysftp.Connection(ftp_europastry,
						username=ftp_user,
						password=ftp_pass,
						cnopts=cnopts,
						) as sftp:
			_logger.error(local_path)
			_logger.error(destino)
			sftp.put(local_path,destino)



		return

	@api.model
	def gen_seguimiento_europ(self):
		now = datetime.now()
		
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		_logger.error('inicia gen_seguimiento_europ -- '+date)
		orders=self.env['sale.order'].search([('is_europastry','=',True),('state','!=','cancel')])


		for order in orders:
			lines=self.env['sale.order.line'].search([('order_id','=',order.id)])
			_logger.error('lineas '+ str(lines))

			for pick in order.picking_ids:
				picking=pick

			date2=""
			fecha_entregado=""
			if picking.date_done:
				date2=datetime.strptime(picking.date_done, '%Y-%m-%d %H:%M:%S')
				fecha_entregado =date2.strftime("%d/%m/%Y")
				date2= date2-timedelta(days=2)
				date2 =date2.strftime("%Y-%m-%d %I:%M:%S")

			_logger.error('fecha albaran--- hoy '+ now.strftime("%Y-%m-%d %I:%M:%S")+' Fecha mas dos '+ str(date2))
			if (picking.date_done == False or date2 <= now.strftime("%Y-%m-%d %I:%M:%S")):
				_logger.error('nombre albaran '+str(picking.name))
				for line in lines:

					self.create({
						'cod_dist' : 436381,
						'n_pedido_eurp' :str(order.europastry_order or ""),
						'tip_ped' : "E",
						'cod_cli' : int(order.partner_id.ref[4:]),
						'fecha_entrega_s' : order.fecha_intro or "",
						'fecha_entrega_t' : order.fecha_entrega_t or "",
						'fecha_entrega_r' : fecha_entregado,						
						'cod_articulo' : str(line.product_id.default_code or ""),				
						'cantidad' : int(line.product_uos_qty),
						'unidad_med' : str(line.product_uos.name or ""),					
						'cancelada' : "N",					
						'obser' : ' ',					
					})

		return

