from openerp import models, fields,api
from openerp.osv.expression import get_unaccent_wrapper
import logging

_logger = logging.getLogger(__name__)



class resPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.One2many(comodel_name='product.supplierinfo',
                                   inverse_name='name',
                                   string='Company',
                                  )

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):

            self.check_access_rights(cr, uid, 'read')
            where_query = self._where_calc(cr, uid, args, context=context)
            self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(cr)


            query = """SELECT id
                         FROM res_partner
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {comercial} {operator} {percent}
                           OR {ref} {operator} {percent}
                           OR {vat} {operator} {percent})
                     ORDER BY {display_name}
                    """.format(where=where_str, operator=operator,
                               email=unaccent('email'),
                               display_name=unaccent('display_name'),
                               comercial=unaccent('comercial'),
                               ref=unaccent('ref'),
                               vat=unnacent('vat'),
                               percent=unaccent('%s'))

            where_clause_params += [search_name,search_name,search_name,search_name,search_name]
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], cr.fetchall())

            if ids:
                return self.name_get(cr, uid, ids, context)
            else:
                return []
        return super(resPartner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

   
   

    def name_get(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name = "%s, %s" % (record.parent_name, name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            if record.comercial:
              name = '('+record.comercial.strip()+') '+name
            res.append((record.id, name))
        return res

