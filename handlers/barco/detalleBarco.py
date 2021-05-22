import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.barco import Barco


class detalleBarcoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            try:
                id_barco = self.request.GET["id_barco"]
            except:
                id_barco = "ERROR"

            if id_barco != "ERROR":
                try:
                    barco = ndb.Key(urlsafe=id_barco).get()
                    if barco:
                        user_name = user.nickname()
                        lista_comentarios = Comentario.query(Comentario.id_vehiculo == barco.key).order(
                            -Comentario.fecha)
                        template_values = {
                            "user_name": user_name,
                            "barco": barco,
                            "lista_comentarios": lista_comentarios,
                            "users": users
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(
                            jinja.render_template("/barco/detalleBarco.html", **template_values))
                    else:
                        mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                        url = "/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                except:
                    mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                    url = "/verBarcos"

                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
            else:
                mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
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

    def post(self):
        user = users.get_current_user()

        if user:
            if not users.is_current_user_admin():
                id_barco = self.request.get("edIdBarco", "ERROR")
                contenidoComentario = self.request.get("edComentario", "ERROR")
                puntuacion = self.request.get("edPuntuacion", "ERROR")
                if id_barco == "ERROR" or contenidoComentario == "ERROR" or puntuacion == "ERROR":
                    mensaje = "ERROR al procesar su comentario, disculpe las molestias"
                    url = "/verBarcos"

                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    barco = ndb.Key(urlsafe=id_barco).get()
                    comentario = Comentario(user_name=user.nickname(), contenido=contenidoComentario,
                                            id_vehiculo=barco.key, puntuacion = int(puntuacion))
                    comentario.put()
                    url = "/detalleBarco?id_barco=" + id_barco
                    mensaje = "Su comentario para el barco '" + barco.nombre + "' ha sido guardado con exito"
                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }
                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("mensajeGenerico.html", **template_values))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/detalleBarco', detalleBarcoHandler),
], debug=True)