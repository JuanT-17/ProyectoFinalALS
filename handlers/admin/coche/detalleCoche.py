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
            if users.is_current_user_admin():
                try:
                    id_coche = self.request.GET["id_coche"]
                except:
                    id_coche = "ERROR"
                if id_coche != "ERROR":
                    try:
                        coche = ndb.Key(urlsafe=id_coche).get()
                        if coche:
                            user_name = user.nickname()
                            lista_comentarios = Comentario.query(Comentario.id_vehiculo == coche.key).order(-Comentario.fecha)
                            template_values = {
                                "user_name": user_name,
                                "coche": coche,
                                "lista_comentarios": lista_comentarios
                            }

                            jinja = jinja2.get_jinja2(app=self.app)
                            self.response.write(jinja.render_template("/admin/coche/detalleCoche.html", **template_values))
                        else:
                            mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                            url = "/admin/verCoches"

                            template_values = {
                                "mensaje": mensaje,
                                "url": url
                            }

                            jinja = jinja2.get_jinja2(app=self.app)
                            self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                    except:
                        mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                        url = "/admin/verCoches"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "ERROR al acceder al vehiculo solicitado, disculpe las molestias"
                    url = "/admin/verCoches"

                    template_values = {
                        "mensaje" : mensaje,
                        "url" : url
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
    ('/admin/detalleCoche', detalleCocheHandler),
], debug=True)