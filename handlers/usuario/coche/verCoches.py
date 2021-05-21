import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche


class verCochesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        lista_coches = Coche.query()
        if user:
            if not users.is_current_user_admin():
                user_name = user.nickname()
                template_values = {
                    "user_name": user_name,
                    "lista_coches": lista_coches
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("/usuario/coche/listadoCoches.html", **template_values))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/verCoches', verCochesHandler),
], debug=True)