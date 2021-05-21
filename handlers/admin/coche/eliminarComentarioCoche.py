import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.comentario import Comentario
from model.coche import Coche



class adminEliminarComentarioCocheHandler(webapp2.RequestHandler):
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
                        "id_coche": comentario.id_vehiculo.urlsafe()
                    }

                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(
                        jinja.render_template("/admin/coche/eliminarComentario.html", **template_values))
                except:
                    mensaje = "Ha ocurrido un error inesperado, disculpe las molestias"
                    url = "/admin/verCoches"

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
                id_coche = self.request.get("edIdCoche", "ERROR")
                if id_comentario == "ERROR" or id_coche == "ERROR":
                    self.redirect("/")
                    return
                else:
                    comentario = ndb.Key(urlsafe=id_comentario).get()
                    url = "/admin/detalleCoche?id_coche="+comentario.id_vehiculo.urlsafe()
                    mensaje = "El comentario \""+comentario.contenido+"\" ha sido eliminado con exito"
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
    ('/admin/eliminarComentarioCoche', adminEliminarComentarioCocheHandler),
], debug=True)