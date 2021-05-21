import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche

class adminEditarBarcoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                try:
                    id_barco = self.request.GET["id_barco"]
                except:
                    id_barco = "ERROR"
                if id_barco != "ERROR":
                    try:
                        barco = ndb.Key(urlsafe=id_barco).get()
                        if barco:
                            template_values = {
                                "user_name": user.nickname(),
                                "barco": barco
                            }

                            jinja = jinja2.get_jinja2(app=self.app)
                            self.response.write(jinja.render_template("/admin/barco/editarBarco.html", **template_values))
                    except:
                        mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                        url = "/admin/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                    url = "/admin/verBarcos"

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

    def post(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                id_barco = self.request.get("edIdBarco", "ERROR")
                nombre = self.request.get("edNombre", "ERROR")
                eslora = self.request.get("edEslora", "ERROR")
                tipo_embarcacion = self.request.get("edTipoEmbarcacion", "ERROR")
                num_pasajeros = self.request.get("edNumPasajeros", "ERROR")

                if nombre != "ERROR" and eslora != "ERROR" and tipo_embarcacion != "ERROR" and \
                        num_pasajeros != "ERROR" and id_barco != "ERROR":
                    try:
                        barco = ndb.Key(urlsafe=id_barco).get()
                        barco.nombre = nombre
                        barco.eslora = int(eslora)
                        barco.tipo_embarcacion = tipo_embarcacion
                        barco.num_pasajeros = int(num_pasajeros)
                        barco.put()

                        mensaje = "El barco con nombre \"" + barco.nombre.capitalize() + "\" ha sido editado con exito"
                        url = "/admin/detalleBarco?id_barco="+id_barco

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                    except:
                        mensaje = "Error inesperado al recuperar datos del formulario"
                        url = "/admin/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "Error inesperado al recuperar datos del formulario"
                    url = "/admin/verBarcos"

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
    ('/admin/editarBarco', adminEditarBarcoHandler),
], debug=True)
