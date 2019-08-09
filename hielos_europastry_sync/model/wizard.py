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



class europastry_informe(models.TransientModel):
	_name = "europastry.informe"

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
	fecha_inicio=fields.Date(string=_('Fecha desde'))
	fecha_fin=fields.Date(string=_('Fecha hastag'))


	@api.multi
	def report_europastry_informe(self,data):

		
		# datas = {	'doc_ids':ids,
		# 			'model': 'europastry.informe',
		# 			'docs':self,		
		# 		}
		#data['form'].update(self.read(['cod_cli'])[0])
        #return self.env['report'].get_action(self, 'sales_report.report_salesperson', data=data)
		
		data={'fecha_inicio':self.fecha_inicio,'fecha_fin':self.fecha_fin}
		
		return self.env['report'].get_action(self,'hielos_europastry_sync.report_europastry_entrega_ids',data=data)
		# report_obj = self.env['report']
		
		# report = report_obj._get_report_from_name('hielos_europastry_sync.report_europastry_entrega_ids')
		# docargs = {
		# 	'doc_ids' : docids,
		# 	'doc_model': report.model,
		# 	'docs': self,
		# 	'custom':po_obj,
		# }
		# return report_obj.render('hielos_europastry_sync.report_europastry_entrega_ids', docargs)

class ReportSalesperson(models.AbstractModel):
	_name = 'report.hielos_europastry_sync.report_europastry_entrega_ids'
	
	@api.model
	def render_html(self, docids, data):

		informe=self.env['europastry.informe']
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_id'))
		now = datetime.now()

		date = str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		_logger.error('################ inicia print report '+str(data['fecha_fin']))
		ids=[]
		fstart=data['fecha_inicio']
		#fstart=fstart.strftime("%Y-%m-%d %I:%M:%S")
		fend=data['fecha_fin']
		#fend =fend.strftime("%Y-%m-%d %I:%M:%S")
		_logger.error('############# fecha fin  '+str(fend))
		date=str(now.day).zfill(2)+str(now.month).zfill(2)+str(now.year)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
		pickings=self.env['stock.picking'].search([('state','!=','cancel'),('state','!=','draft'),'|',('date_done','>',fstart),('date_done','=',False),'|',('date_done','<',fend),('date_done','=',False)])
		_logger.error('Albaranes '+str(pickings))
		for picking in pickings:
			#lines=self.env['stock.move'].search([('picking_id','=',picking.id)])
			#order=self.env['sale.order'].search([('name','=',picking.origin)])
			
			for line in picking.move_lines:
				
				nombre_categ="EP-PRODUCTOS EUROPASTRY"
				product_categ=line.product_id.categ_id.name
				#_logger.error('es europastry' + product_categ.strip()+' == '+nombre_categ.strip()+' es ')
				#_logger.error(product_categ.strip() == nombre_categ.strip())
				if (product_categ.strip() == nombre_categ.strip()):
					#_logger.error('si' + line.product_id.name)
					lotes=""
					for lote in line.lot_ids:
						lotes=lotes+", "+lote.name

					same_line=informe.search([('procesada','=',False),('lote','=',lotes),('cod_cli','=',int(picking.partner_id.ref[4:])),('num_alb','=',str(picking.europastry_pick)),('cod_articulo','=',str(line.product_id.default_code)),('unidad_med','=',str(line.product_uom.name))])
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
						
						id_created=informe.create({
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
						
						ids.append(id_created.id)
		
		
		obj=informe.search([('id','in',ids)])
		_logger.error("####################### ids "+str(ids))
		docargs = {
			'doc_ids': self.ids,
			'doc_model': self.model,
			'docs': docs,
			'custom': obj
		}
		return self.env['report'].render('hielos_europastry_sync.report_europastry_entrega_ids', docargs)
