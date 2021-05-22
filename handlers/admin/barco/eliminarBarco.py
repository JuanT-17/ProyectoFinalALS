import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.barco import Barco


class eliminarBarcoHandler(webapp2.RequestHandler):
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

                        user_name = user.nickname()
                        template_values = {
                            "user_name": user_name,
                            "barco" : barco
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/admin/barco/eliminarBarco.html", **template_values))
                    except:
                        mensaje = "Error inesperado, disculpe las molestias"
                        url = "/verBarcos"

                        template_values = {
                            "mensaje": mensaje,
                            "url": url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("/mensajeGenerico.html", **template_values))
                else:
                    mensaje = "Error inesperado, disculpe las molestias"
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

    def post(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                id_barco = self.request.get("edIdBarco", "ERROR")
                if id_barco == "ERROR":
                    self.redirect("/")
                    return
                else:
                    try:
                        barco = ndb.Key(urlsafe=id_barco).get()
                        lista_comentarios = Comentario.query(Comentario.id_vehiculo == barco.key)

                        url = "/verBarcos"
                        mensaje = "El barco de nombre \""+barco.nombre+"\" y todos sus comentarios asociados "+"" \
                                  "han sido eliminados con exito"
                        barco.key.delete()
                        for comentario in lista_comentarios:
                            comentario.key.delete()
                        template_values = {
                            "mensaje": mensaje,
                            "url" : url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("mensajeGenerico.html", **template_values))
                    except:
                        mensaje = "Error inesperado, disculpe las molestias"
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
    ('/eliminarBarco', eliminarBarcoHandler),
], debug=True)