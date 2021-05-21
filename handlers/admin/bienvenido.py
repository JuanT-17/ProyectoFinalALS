import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


class AdminBienvenidoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                user_name = user.nickname()
                template_values = {
                    "user_name": user_name
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("/admin/bienvenido.html", **template_values))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return

app = webapp2.WSGIApplication([
    ('/admin/bienvenido', AdminBienvenidoHandler),
], debug=True)