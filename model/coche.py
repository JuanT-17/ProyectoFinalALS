from google.appengine.ext import ndb


class Coche(ndb.Model):
    nombre = ndb.StringProperty(required=True, indexed=True)
    marca = ndb.StringProperty(required=True, indexed=True)
    num_puertas = ndb.IntegerProperty(required=True)
    caballos = ndb.IntegerProperty(required=True)
    combustible = ndb.StringProperty(required=True, indexed=True)
    num_asientos = ndb.IntegerProperty(required=True)


