import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche


class eliminarCocheHandler(webapp2.RequestHandler):
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

                    user_name = user.nickname()
                    template_values = {
                        "user_name": user_name,
                        "coche" : coche
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(jinja.render_template("/admin/coche/eliminarCoche.html", **template_values))
                except:
                    mensaje = "Error inesperado, disculpe las molestias"
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
                id_coche = self.request.get("edIdCoche", "ERROR")
                if id_coche == "ERROR":
                    self.redirect("/")
                    return
                else:
                    coche = ndb.Key(urlsafe=id_coche).get()
                    lista_comentarios = Comentario.query(Comentario.id_vehiculo == coche.key)

                    url = "/verCoches"
                    mensaje = "El coche de nombre \""+coche.nombre+"\" y todos sus comentarios asociados "+"" \
                              "han sido eliminados con exito"
                    coche.key.delete()
                    for comentario in lista_comentarios:
                        comentario.key.delete()
                    template_values = {
                        "mensaje": mensaje,
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
    ('/eliminarCoche', eliminarCocheHandler),
], debug=True)