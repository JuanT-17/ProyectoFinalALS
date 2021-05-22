import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche

class editarCocheHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                try:
                    id_coche = self.request.GET["id_coche"]
                except:
                    id_coche = "ERROR"
                try:
                    coche = ndb.Key(urlsafe=id_coche).get()
                    if coche:
                        template_values = {
                            "user_name": user.nickname(),
                            "coche": coche
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/admin/coche/editarCoche.html", **template_values))
                except:
                    mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
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
                id_coche = self.request.get("edIdCoche", "ERROR")

                if nombre != "ERROR" and marca != "ERROR" and num_puertas != "ERROR" and \
                        caballos != "ERROR" and combustible != "ERROR" and num_asientos != "ERROR"\
                        and id_coche != "ERROR":
                    try:
                        coche = ndb.Key(urlsafe=id_coche).get()
                        coche.nombre = nombre
                        coche.marca = marca
                        coche.num_puertas = int(num_puertas)
                        coche.caballos = int(caballos)
                        coche.combustible = combustible
                        coche.num_asientos = int(num_asientos)
                        coche.put()

                        mensaje = "El coche con nombre \"" + coche.nombre.capitalize() + "\" ha sido editado con exito"
                        url = "/detalleCoche?id_coche="+id_coche

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
    ('/editarCoche', editarCocheHandler),
], debug=True)
