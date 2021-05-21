import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.barco import Barco



class adminEliminarComentarioBarcoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                try:
                    id_comentario = self.request.GET["id_comentario"]
                    comentario = ndb.Key(urlsafe=id_comentario).get()
                    user_name = user.nickname()
                    template_values = {
                        "user_name": user_name,
                        "comentario": comentario,
                        "id_barco": comentario.id_vehiculo.urlsafe()
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(
                        jinja.render_template("/admin/barco/eliminarComentarioBarco.html", **template_values))
                except:
                    mensaje = "Ha ocurrido un error inesperado, disculpe las molestias"
                    url = "/admin/verBarcos"

                    template_values = {
                        "mensaje": mensaje,
                        "url": url
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(
                        jinja.render_template("/mensajeGenerico.html", **template_values))
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
                id_comentario = self.request.get("edIdComentario", "ERROR")
                id_barco = self.request.get("edIdBarco", "ERROR")
                if id_comentario == "ERROR" or id_barco == "ERROR":
                    self.redirect("/")
                    return
                else:
                    try:
                        comentario = ndb.Key(urlsafe=id_comentario).get()
                        url = "/admin/detalleBarco?id_barco="+comentario.id_vehiculo.urlsafe()
                        mensaje = "El comentario \""+comentario.contenido+"\" ha sido eliminado con exito"
                        comentario.key.delete()
                        template_values = {
                            "mensaje": mensaje,
                            "url" : url
                        }

                        jinja = jinja2.get_jinja2(app=self.app)
                        self.response.write(jinja.render_template("mensajeGenerico.html", **template_values))
                    except:
                        url = "/admin/verBarcos"
                        mensaje = "Error inesperado, disculpe las molestias"
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
    ('/admin/eliminarComentarioBarco', adminEliminarComentarioBarcoHandler),
], debug=True)