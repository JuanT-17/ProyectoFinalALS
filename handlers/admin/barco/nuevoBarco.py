import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.barco import Barco


class nuevoBarcoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                template_values = {
                    "user_name": user.nickname()
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("/admin/barco/nuevoBarco.html", **template_values))
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
                eslora = self.request.get("edEslora", "ERROR")
                tipo_embarcacion = self.request.get("edTipoEmbarcacion", "ERROR")
                num_pasajeros = self.request.get("edNumPasajeros", "ERROR")

                if nombre != "ERROR" and eslora != "ERROR" and tipo_embarcacion != "ERROR" and \
                        num_pasajeros != "ERROR":
                    try:
                        barcoNuevo = Barco(nombre=nombre.lower(), eslora=int(eslora), tipo_embarcacion=tipo_embarcacion,\
                                           num_pasajeros=int(num_pasajeros))
                        barcoNuevo.put()

                        mensaje = "El barco con nombre \"" + barcoNuevo.nombre.capitalize() + "\" ha sido almacenado" \
                                                                                              " con exito"
                        url = "/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                    except:
                        mensaje = "ERROR al recuperar datos del formulario, disculpe las molestias"
                        url = "/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "Error inesperado al recuperar datos del formulario"
                    url = "/verBarcos"

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
    ('/nuevoBarco', nuevoBarcoHandler),
], debug=True)
