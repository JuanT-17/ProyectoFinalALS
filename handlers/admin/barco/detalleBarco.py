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
            if users.is_current_user_admin():
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
                                "lista_comentarios": lista_comentarios
                            }

                            jinja = jinja2.get_jinja2(app=self.app)
                            self.response.write(
                                jinja.render_template("/admin/barco/detalleBarco.html", **template_values))
                        else:
                            mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                            url = "/admin/verBarcos"

                            template_values = {
                                "mensaje": mensaje,
                                "url": url
                            }

                            jinja = jinja2.get_jinja2(app=self.app)
                            self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
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

app = webapp2.WSGIApplication([
    ('/admin/detalleBarco', detalleBarcoHandler),
], debug=True)