import logging
import time
import datetime
from datetime import timedelta
from openerp.tools import ustr
import unicodedata

from openerp.osv import fields, orm, osv


_logger = logging.getLogger(__name__)


class export_control(osv.osv):
    _inherit = 'export.control'
    _name = "export.control"
    #=================== 716 Rutero              ==================================
    # def _create_report716(self, cr, uid, ids, context=None):
    #     if context is None:
    #         context = {}
    #     par_obj = self.pool.get('ruta')
    #     search_condition = [('tercap_incluir', '=', True)]
    #     part_selec_obj = par_obj.search(cr, uid, search_condition )
     
    #     output = ''
    #     for ruta in part_selec_obj:
    #         visita = 0                          
    #         line = par_obj.browse(cr, uid, ruta)
    #         if line.partner_rutas_ids:
    #             _logger.error('dias_visita')
    #             _logger.error(str(line.dias_visita))
    #             for mdays in line.dias_visita:
    #                 for c in line.partner_rutas_ids: 
    #                     #Manuel modificado el 28-3-16 para usar el codigo de ruta de Tercap
    #                     #codruta= str(line.id).zfill(4)
    #                     codruta= str(line.cod_tercap).zfill(4)
    #                     codcliente= str(c.id).zfill(9)
    #                     coddireccion = str(c.id).zfill(9)
    #                     diavisita = str(mdays.cod_day).zfill(9) #if line.dias_visita else '000000000'
    #                     #19-4-16 se gestiona un nuevo campo en la ficha de cliente: el orden de visita en el dia
    #                     if (c.orden_visita<>0):
    #                         ordenvisita = str(int(c.orden_visita)).zfill(9)
    #                     else: 
    #                         ordenvisita = str(visita + 1).zfill(9)               
    #                     frecuencia = line.frecuencia if line.frecuencia else 'S'
    #                     codclialternativo = ' '
    #                     coddirealternativo = ' '
            
    #                     fields_fields_716 = [
    #                     codruta,
    #                     codcliente,
    #                     coddireccion,
    #                     diavisita,
    #                     ordenvisita, 
    #                     frecuencia,
    #                     codclialternativo,
    #                     coddirealternativo,                   
    #                                   ]       
    #                     fields_716 = ';'.join(['%s' % one_field for one_field in fields_fields_716])
    #                     output += fields_716.encode('CP1252') + '\n'
            
    #     _logger.error('######## output' + output)
    #     filename = '/var/ftp/ERP/RUTERO'
    #     formato = 'txt'
    #     nombre = "%s.%s" % (filename, formato)
    #     #out = base64.encodestring(output)
    #     outfile = open(nombre, 'w')
    #     outfile.write(output)
    #     outfile.close()
    #     return

class tercap_days(osv.osv):
    _name="tercap.days"

    _columns = {
        'name': fields.char('Nombre dia semana'),
        'cod_day': fields.integer('Numero dia semana'),
    }

class ruta(osv.osv):

    _inherit="ruta"

    _columns = {'dias_visita':fields.many2many('tercap.days',string='Dias de visita')}