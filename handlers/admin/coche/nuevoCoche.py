import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche


class nuevoCocheHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                template_values = {
                    "user_name": user.nickname()
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("admin/coche/nuevoCoche.html", **template_values))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                nombre = self.request.get("edNombre", "ERROR")
                marca = self.request.get("edMarca", "ERROR")
                num_puertas = self.request.get("edPuertas", "ERROR")
                caballos = self.request.get("edCaballos", "ERROR")
                combustible = self.request.get("edCombustible", "ERROR")
                num_asientos = self.request.get("edNumAsientos", "ERROR")

                if nombre != "ERROR" and marca != "ERROR" and num_puertas != "ERROR" and \
                        caballos != "ERROR" and combustible != "ERROR" and num_asientos != "ERROR":
                    try:
                        cocheNuevo = Coche(nombre=nombre.lower(), marca=marca.lower(), num_puertas=int(num_puertas),
                                           caballos=int(caballos), combustible=combustible.lower(),
                                           num_asientos=int(num_asientos))
                        cocheNuevo.put()

                        mensaje = "El coche con nombre \"" + cocheNuevo.nombre.capitalize() + "\" ha sido almacenado" \
                                                                                              " con exito"
                        url = "/verCoches"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                    except:
                        mensaje = "Error inesperado al recuperar datos del formulario"
                        url = "/verCoches"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "Error inesperado al recuperar datos del formulario"
                    url = "/verCoches"

                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))

            else:
                self.redirect("/")
                return

        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/nuevoCoche', nuevoCocheHandler),
], debug=True)
