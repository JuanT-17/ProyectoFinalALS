import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche


class adminVerCochesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                user_name = user.nickname()
                lista_coches = Coche.query()
                template_values = {
                    "user_name": user_name,
                    "lista_coches": lista_coches
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("/admin/coche/listadoCoches.html", **template_values))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/admin/verCoches', adminVerCochesHandler),
], debug=True)