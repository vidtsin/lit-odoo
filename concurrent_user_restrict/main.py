import openerp
from openerp import http
from openerp.addons.web.controllers.main import Home
from openerp import SUPERUSER_ID
import werkzeug.utils
from openerp.http import request
x_username={}
Warning_shown = []
db_list = http.db_list
class user_logout(Home):
     @http.route('/web/login', type='http', auth="none")
     def web_login(self, redirect=None, **kw):
        values = request.params.copy()
        session_store1=openerp.tools.config.filestore(request.session.db)
        print "session stope pathsssssssssssssssssssssssssssss",session_store1
        
        try:
            print "here in try"
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None
        
        if request.httprequest.method == 'POST':
            database_name=request.session.db
# user name and password are authenticated below
# if uid is true number of allowed concurrent user is fetched
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
				
                cr = openerp.sql_db.db_connect(database_name).cursor()   
                pool=openerp.pooler.RegistryManager.get(database_name)
                status_check=pool.get("res.users").search(cr, SUPERUSER_ID,[('x_login_status_1', '=',True)],context=None)
                count=len(status_check)
                cr.close()
                print "here in false"
                cr = openerp.sql_db.db_connect(database_name).cursor()   
                pool=openerp.pooler.RegistryManager.get(database_name)
                status_check=pool.get("custom.config.settings").browse(cr,SUPERUSER_ID,SUPERUSER_ID,context=None)
                print "here in false after"
                status=status_check.x_no_of_concurrent_users
                cr.close()
                if count < status:
					cr = openerp.sql_db.db_connect(database_name).cursor()
					pool=openerp.pooler.RegistryManager.get(database_name)
					result=pool.get("res.users").write(cr,SUPERUSER_ID,uid,{'x_login_status_1':True})
					cr.commit()
					cr.close()
					return super(user_logout,self).web_login(redirect=None, **kw)
                elif uid == SUPERUSER_ID:
					return super(user_logout,self).web_login(redirect=None, **kw)
                else:
                    values['error'] = "SUPERADO EL NUMERO DE USUARIOS CONCURRENTES!!"
					 # values['error'] = "Maximum number of Concurrent users reached" 
                    return request.render('web.login', values)
            else:
                values['error'] = "ERROR DE CREDENCIALES"
                 # values['error'] = "Wrong Credentials"  
                return request.render('web.login', values)
        else:
            values['error'] = "Esperando datos de conexion"
             # values['error'] = "You are Logged Out"
            return request.render('web.login', values)
                      
         
     @http.route('/web/session/logout', type='http', auth="none")
     def logout(self, redirect='/web'):
         print "supperrrrrrrrrrrrrrrrrrrrrrrrrrrr",SUPERUSER_ID
#          print "logout session is",request.session.sid
         database_name=request.session.db
         uid=request.session.uid
         pool=openerp.pooler.RegistryManager.get(database_name)
         cr = openerp.sql_db.db_connect(database_name).cursor()
         result=pool.get("res.users").write(cr,SUPERUSER_ID,uid,{'x_login_status_1':False})
         cr.commit()
         cr.close()
         print "Warning_shown-------------------------------logout",Warning_shown
         if uid in Warning_shown:
             print "Warning_shown-------------------------------logging out uid",Warning_shown
             Warning_shown.remove(uid)
         request.session.logout(keep_db=True)
         return werkzeug.utils.redirect(redirect, 303)
        

   
