import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche


class detalleCocheHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            try:
                id_coche = self.request.GET["id_coche"]
            except:
                id_coche = "ERROR"

            if id_coche != "ERROR":
                try:
                    coche = ndb.Key(urlsafe=id_coche).get()
                    if coche:
                        user_name = user.nickname()
                        lista_comentarios = Comentario.query(Comentario.id_vehiculo == coche.key).order(
                            -Comentario.fecha)
                        template_values = {
                            "user_name": user_name,
                            "coche": coche,
                            "lista_comentarios": lista_comentarios,
                            "users" : users
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(
                            jinja.render_template("/coche/detalleCoche.html", **template_values))
                    else:
                        mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                        url = "/verCoches"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
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

    def post(self):
        user = users.get_current_user()

        if user:
            if not users.is_current_user_admin():
                id_coche = self.request.get("edIdCoche", "ERROR")
                contenidoComentario = self.request.get("edComentario", "ERROR")
                puntuacion = self.request.get("edPuntuacion", "ERROR")
                if id_coche == "ERROR" or contenidoComentario == "ERROR" or puntuacion == "ERROR":
                    mensaje = "ERROR al procesar su comentario, disculpe las molestias"
                    url = "/verCoches"

                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    coche = ndb.Key(urlsafe=id_coche).get()
                    comentario = Comentario(user_name=user.nickname(), contenido=contenidoComentario,
                                            id_vehiculo=coche.key, puntuacion = int(puntuacion))
                    comentario.put()
                    url = "/detalleCoche?id_coche="+id_coche
                    mensaje = "Su comentario para el coche '"+coche.nombre+"' ha sido guardado con exito"
                    template_values = {
                        "mensaje" : mensaje,
                        "url" : url
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
    ('/detalleCoche', detalleCocheHandler),
], debug=True)