# IntegraVehiculo
# Proyecto final para la asignatura de ALS en la ESEI

#Pagina de bienvenida se comprueba si el usuario existe y si es o no admin


import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb


class User(ndb.Model):
    id_user = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.redirect("/bienvenido")
            return
        else:
            access_link = users.create_login_url("/")

        template_values = {
            "access_link": access_link
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("login.html", **template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)

