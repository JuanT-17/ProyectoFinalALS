from google.appengine.ext import ndb


class Barco(ndb.Model):
    nombre = ndb.StringProperty(required=True, indexed=True)
    eslora = ndb.IntegerProperty(required=True)
    tipo_embarcacion = ndb.StringProperty(required=True, indexed=True)
    num_pasajeros = ndb.IntegerProperty(required=True)