from openerp import SUPERUSER_ID
from openerp.osv import fields, osv



class CustomSettings(osv.Model):
    _name = 'custom.config.settings'
    _inherit ='res.config.settings'
    _columns = {
            'x_no_of_concurrent_users':fields.integer('No of Concurrent Users Logins allowed',default=1)
                }
	
    def get_default_CustomSettings(self, cr, uid, fields, context=None):
    	user_name=self.pool.get('custom.config.settings').browse(cr,SUPERUSER_ID, uid, context=context).x_no_of_concurrent_users
        return {'x_no_of_concurrent_users': user_name}

    def set_default_CustomSettings(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        new_username=config.x_no_of_concurrent_users
        self.pool.get('custom.config.settings').write(cr,SUPERUSER_ID, uid, {'x_no_of_concurrent_users': new_username})



class res_users(osv.Model):
    _inherit = 'res.users'
    _columns = {
            'x_login_status_1': fields.boolean('x_login_status'),
                }   




