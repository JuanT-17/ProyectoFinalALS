from google.appengine.ext import ndb

class Comentario(ndb.Model):
    contenido = ndb.StringProperty(required=True)
    fecha = ndb.DateTimeProperty(auto_now_add=True)
    user_name = ndb.StringProperty(required=True)
    id_vehiculo = ndb.KeyProperty(required=True)
    puntuacion = ndb.IntegerProperty(required=True)