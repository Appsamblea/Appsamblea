#Sistema de despliegue continuo

El sistema de despliegue continuo tiene que subir a App Engine todo el contenido de la aplicación en Django cada vez que se haga un pull a la rama Master.

##Opción 1: Conectar un repositorio externo desde Google Developers Console

Accediendo a la Google Developers Console podemos conectar un repositorio externo, de forma que se duplica todo lo que haya en dicho repositorio.

Se prueba a conectar este repositorio para ver qué ocurre. Sin embargo no conecta nada, debido a que solo se puede tener código fuente dentro del repositorio, y este contiene más cosas.

##Opción 2: [Shippable](https://www.shippable.com/)

Se comentó en clase esta opción para despliegue continuo. Por ello tras no poder hacerlo con Google Developers Console se intenta con esta opción.

Primero pide permisos para acceder a la cuenta de Github. A continuación se le dice con qué repositorio trabajar.  

Sin embargo hace falta cierta preparación del repositorio. Por ello se sigue [este tutorial](http://docs.shippable.com/en/latest/start.html).

Primero se crea un fichero shippable.yml, utilizando [este](https://github.com/shippableSamples/sample-django-cloudsql-appengine/blob/master/shippable.yml) como ejemplo.

Sin éxito se encuentran varios ejemplos y se crea un pequeño fichero que ejecutará test.py.

Como se necesita una estructura de ficheros compatible con un proyecto de Django se restructura por completo el repositorio.





