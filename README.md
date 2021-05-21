# Proyecto final de ALS.

### Juan Tenorio Costa


El siguiente código responde a la entrega final para la asignatura de 4º curso de la ESEI en Ingeniería infórmatica ALS
(Aplicaciones con lenguajes de Script). Trata del desarrollo de una aplicación Web


La aplicación sirve para la visualización y gestión de barcos y coches donde a los usuarios se les permite comentar
sobre ellos.


La aplicación distingue dos tipos de Usuarios:

1) Administradores o moderadores (a partir de aquí se referenciarán como Admins).

2) Usuarios estándar (a partir de aquí se referenciarán como Users).

Los Admins pueden acceder al listado de coches o barcos, ver en detalle cualquiera de ellos, editar sus datos, borrar
alguno de ellos (implicando el borrado de todos los comentarios asociados) o borrar algún comentario asociado concreto.
A los Admins no se les permite comentar en los vehículos.

Los Users pueden acceder al listado de coches o barcos, ver en detalle cualquiera de ellos y comentar en cualquiera de 
ellos, además pueden borrar sus comentarios pero no los de otros usuarios. A un User no se le permite ni borrar ni 
editar ni añadir nuevos vehículos a la aplicación.

##Ejecución

El entorno de ejecución fue el indicado en clase.

Como IDE PyCharm con Python 2.7, uso de Google Cloud para utilizar el Google Application Engine .

La aplicación no acepta el uso de tildes ni caracteres especiales como la 'ñ' en ningún momento.

Una vez se está ejecutando en PyCharm la aplicación es accesible a través de las siguientes direcciones:

1) http://127.0.0.1:8080 : Aplicación Web

2) http://localhost:8000 : Consola de administración