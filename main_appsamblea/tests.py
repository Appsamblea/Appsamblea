# -*- encoding: utf-8 -*-
import django.core.handlers.wsgi
from google.appengine.ext import testbed
from main_appsamblea.models import *
import webtest


class AppsambleaTestCase(django.test.TestCase):
    def setUp(self):
        # Primero, crear una instancia de la clase Testbed.
        self.testbed = testbed.Testbed()
        # Activar testbed, que prepara los stub de los servicios para su uso.
        self.testbed.activate()
        # Luego, declara que stubs de servicios quieres usar.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testapp = webtest.TestApp(django.core.handlers.wsgi.WSGIHandler())

        # Usuario común
        usuarioTest = Usuario(password="", username="usuarioTest", first_name="", last_name="", fecha_nac="2013-12-13",
                              telefono="", email="", localidad="", pais="", bio="")
        usuarioTest.save()

        # Organización común
        organizacionTest = Organizacion(nombre="organizacionTest", tematica="A")
        organizacionTest.save()

        # Asamblea común
        asambleaTest = Asamblea(nombre="asambleaTest", fecha="2015-01-01", descripcion="Asamblea de prueba",
                                usuario=usuarioTest, organizacion=organizacionTest)
        asambleaTest.save()

        # Grupo común
        grupoTest = Grupo(nombre="grupoTest", descripcion="asdasdasd", organizacion=organizacionTest,
                          administrador=usuarioTest)
        grupoTest.save()

        # Participa común
        participaTest = Participa(usuario=usuarioTest, asamblea=asambleaTest)
        participaTest.save()


        #def tearDown(self):
        self.testbed.deactivate()

    def testActa(self):
        print ("Realizando tests de actas")
        asambleaTest = Asamblea.objects.get(nombre="asambleaTest")

        Acta.objects.create(texto="Asamblea de prueba", asamblea=asambleaTest)
        Acta.objects.create(texto="", asamblea=asambleaTest)

        test1 = Acta.objects.get(texto="Asamblea de prueba")
        test2 = Acta.objects.get(texto="")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El texto está vacío\n")

    def testAsamblea(self):
        print ("Realizando tests de asambleas")
        usuarioTest = Usuario.objects.get(username="usuarioTest")
        organizacionTest = Organizacion.objects.get(nombre="organizacionTest")

        Asamblea.objects.create(nombre="test1", fecha="2013-02-28", descripcion=" ", usuario_id=usuarioTest.id,
                                organizacion=organizacionTest, es_abierta=True)
        Asamblea.objects.create(nombre="", fecha="2013-02-28", descripcion="asdasd", usuario_id=usuarioTest.id,
                                organizacion=organizacionTest, es_abierta=True)
        Asamblea.objects.create(nombre="test3", fecha="2013-12-13", descripcion="asamblea de prueba",
                                usuario_id=usuarioTest.id, organizacion=organizacionTest,
                                url_streaming="http://www.google.es")
        Asamblea.objects.create(nombre="test4", fecha="2013-12-13", descripcion="asamblea de prueba",
                                usuario_id=usuarioTest.id, organizacion=organizacionTest,
                                url_streaming="www.aiurhtaiurutiaert.es")
        Asamblea.objects.create(nombre="test5", fecha="2013-12-13", descripcion="asamblea de prueba",
                                usuario_id=usuarioTest.id, organizacion=organizacionTest,
                                urlasamblea="http://www.google.es")
        Asamblea.objects.create(nombre="test6", fecha="2013-12-13", descripcion="asamblea de prueba",
                                usuario_id=usuarioTest.id, organizacion=organizacionTest,
                                urlasamblea="www.aiurhtaiurutiaert.es")

        test1 = Asamblea.objects.get(nombre="test1")
        test2 = Asamblea.objects.get(descripcion="asdasd")
        test3 = Asamblea.objects.get(nombre="test3")
        test4 = Asamblea.objects.get(nombre="test4")
        test5 = Asamblea.objects.get(nombre="test5")
        test6 = Asamblea.objects.get(nombre="test6")

        self.assertEqual(test1.isOk(), "La descripción debe de estar vacía\n")
        self.assertEqual(test2.isOk(), "El nombre está vacío\n")
        self.assertEqual(test3.isOk(), "")
        self.assertEqual(test4.isOk(), "La URL del streaming no funciona\n")
        self.assertEqual(test5.isOk(), "")
        self.assertEqual(test6.isOk(), "La URL de la asamblea no funciona\n")

    def testDocumento(self):
        print ("Realizando tests de documentos")
        asambleaTest = Asamblea.objects.get(nombre="asambleaTest")

        Documento.objects.create(nombre="test1", url="http://www.google.es", asamblea=asambleaTest)
        Documento.objects.create(nombre="", url="http://www.google.es", asamblea=asambleaTest)
        Documento.objects.create(nombre="test3", url="www.nofunciona.es", asamblea=asambleaTest)

        test1 = Documento.objects.get(nombre="test1")
        test2 = Documento.objects.get(nombre="")
        test3 = Documento.objects.get(nombre="test3")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El nombre no puede estar vacío\n")
        self.assertEqual(test3.isOk(), "La URL del documento no funciona\n")

    def testGrupo(self):
        print ("Realizando tests de grupos")
        organizacionTest = Organizacion.objects.get(nombre="organizacionTest")
        usuarioTest = Usuario.objects.get(username="usuarioTest")

        Grupo.objects.create(nombre="test1", descripcion="asdasd", organizacion=organizacionTest,
                             administrador=usuarioTest)
        Grupo.objects.create(nombre="", descripcion="test2", organizacion=organizacionTest,
                             administrador=usuarioTest)
        Grupo.objects.create(nombre="test3", descripcion="", organizacion=organizacionTest,
                             administrador=usuarioTest)

        test1 = Grupo.objects.get(nombre="test1")
        test2 = Grupo.objects.get(descripcion="test2")
        test3 = Grupo.objects.get(nombre="test3")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El nombre del grupo no puede estar vacío\n")
        self.assertEqual(test3.isOk(), "La descripción del grupo no puede estar vacía\n")

    def testMensaje(self):
        print ("Realizando tests de mensajes")
        usuarioTest = Usuario.objects.get(username="usuarioTest")
        grupoTest = Grupo.objects.get(nombre="grupoTest")

        Mensaje.objects.create(texto="test1", usuario_envia=usuarioTest, usuario_recibe=usuarioTest,
                               grupo=grupoTest)
        Mensaje.objects.create(texto="", usuario_envia=usuarioTest, usuario_recibe=usuarioTest, grupo=grupoTest)

        test1 = Mensaje.objects.get(texto="test1")
        test2 = Mensaje.objects.get(texto="")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El texto no puede estar vacío\n")


    def testOrganizacion(self):
        print ("Realizando tests de organizaciones")
        Organizacion.objects.create(nombre="test1", tematica="tematica", descripcion="asdasdasd",
                                    email="ererererr@asd.com", web="http://www.google.es")
        Organizacion.objects.create(nombre="", tematica="tematica", descripcion="test2",
                                    email="ererererr@asd.com", web="http://www.google.es")
        Organizacion.objects.create(nombre="test3", tematica="", descripcion="asdasdasd",
                                    email="ererererr@asd.com", web="http://www.google.es")
        Organizacion.objects.create(nombre="test4", tematica="tematica", descripcion="",
                                    email="ererererr@asd.com", web="http://www.google.es")
        Organizacion.objects.create(nombre="test5", tematica="tematica", descripcion="asdasdasd",
                                    email="ererererr@asd.com", web="www.iakjrtlajrtoiaer.es")

        test1 = Organizacion.objects.get(nombre="test1")
        test2 = Organizacion.objects.get(descripcion="test2")
        test3 = Organizacion.objects.get(nombre="test3")
        test4 = Organizacion.objects.get(nombre="test4")
        test5 = Organizacion.objects.get(nombre="test5")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El nombre está vacío\n")
        self.assertEqual(test3.isOk(), "La temática está vacía\n")
        self.assertEqual(test4.isOk(), "La descripción está vacía\n")
        self.assertEqual(test5.isOk(), "La URL de la organización no funciona\n")

    def testPunto_orden(self):
        print("Realizando tests de puntos del órden del día")
        asambleaTest = Asamblea.objects.get(nombre="asambleaTest")

        Punto_orden_dia.objects.create(orden=0, nombre="test1", descripcion="asdasd", asamblea=asambleaTest)
        Punto_orden_dia.objects.create(orden=-1, nombre="test2", descripcion="asdasd", asamblea=asambleaTest)
        Punto_orden_dia.objects.create(orden=0, nombre="", descripcion="asdasd", asamblea=asambleaTest)
        Punto_orden_dia.objects.create(orden=0, nombre="test4", descripcion="", asamblea=asambleaTest)

        test1 = Punto_orden_dia.objects.get(nombre="test1")
        test2 = Punto_orden_dia.objects.get(nombre="test2")
        test3 = Punto_orden_dia.objects.get(nombre="")
        test4 = Punto_orden_dia.objects.get(nombre="test4")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El orden del día no puede ser negativo\n")
        self.assertEqual(test3.isOk(), "El nombre no puede estar vacío\n")
        self.assertEqual(test4.isOk(), "La descripción no puede estar vacía\n")

    def testResponsabilidad(self):
        print ("Realizando tests de responsabilidades")
        asambleaTest = Asamblea.objects.get(nombre="asambleaTest")

        Responsabilidad.objects.create(nombre="test1", tipo="asdasd")
        Responsabilidad.objects.create(nombre="", tipo="test2")
        Responsabilidad.objects.create(nombre="test3", tipo="")

        test1 = Responsabilidad.objects.get(nombre="test1")
        test1.asamblea_responsable.add(asambleaTest)
        test2 = Responsabilidad.objects.get(tipo="test2")
        test3 = Responsabilidad.objects.get(nombre="test3")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El nombre no puede estar vacío\n")
        self.assertEqual(test3.isOk(), "El tipo no puede estar vacío\n")

    def testTurno_palabra(self):
        print ("Realizando tests de turnos de palabra")
        usuarioTest = Usuario.objects.get(username="usuarioTest")

        participaTest = Participa.objects.get(usuario=usuarioTest)

        Turno_palabra.objects.create(descripcion="test1", duracion="00:15", duracion_estimada="00:10", orden=1,
                                     participa=participaTest)
        Turno_palabra.objects.create(descripcion="", duracion="00:15", duracion_estimada="00:10", orden=1,
                                     participa=participaTest)
        Turno_palabra.objects.create(descripcion="test3", duracion="00:15", duracion_estimada="00:10", orden=-1,
                                     participa=participaTest)

        test1 = Turno_palabra.objects.get(descripcion="test1")
        test2 = Turno_palabra.objects.get(descripcion="")
        test3 = Turno_palabra.objects.get(descripcion="test3")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "La descripción del turno de palabra no puede estar vacía\n")
        self.assertEqual(test3.isOk(), "El orden del turno de palabra no puede ser inferior a cero\n")

    def testUsuario(self):
        print ("Realizando tests de usuarios")

        Usuario.objects.create(username="test1", password="test1", first_name="test", last_name="asd", fecha_nac="2015-01-01",
                               telefono="958123456", email="prueba@test.com")
        Usuario.objects.create(username="test2", password="", first_name="test", last_name="test2", fecha_nac="2015-01-01",
                               telefono="958123456", email="prueba@test.com")
        Usuario.objects.create(username="test3", password="test3", first_name="", last_name="asd", fecha_nac="2015-01-01",
                               telefono="958123456", email="prueba@test.com")
        Usuario.objects.create(username="test4", password="test4", first_name="test", last_name="", fecha_nac="2015-01-01",
                               telefono="958123456", email="prueba@test.com")
        Usuario.objects.create(username="test5", password="test5", first_name="test5", last_name="asd", fecha_nac="2015-01-01",
                               telefono="958123456", email="prueba@test.com")
        Usuario.objects.create(username="test6", password="test6", first_name="test", last_name="asd", fecha_nac="2015-01-01",
                               telefono="95812ss3456", email="prueba@test.com")

        test1 = Usuario.objects.get(username="test1")
        test2 = Usuario.objects.get(username="test2")
        test3 = Usuario.objects.get(username="test3")
        test4 = Usuario.objects.get(username="test4")
        test5 = Usuario.objects.get(username="test5")
        test6 = Usuario.objects.get(username="test6")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "La contraseña no puede estar vacía\n")
        self.assertEqual(test3.isOk(), "El nombre no puede estar vacío\n")
        self.assertEqual(test4.isOk(), "Los apellidos no pueden estar vacíos\n")
        self.assertEqual(test5.isOk(), "No se pueden incluir números en el nombre\n")
        self.assertEqual(test6.isOk(), "Teléfono mal definido\n")

    def testVotacion(self):
        print("Realizando tests de votaciones")
        usuarioTest = Usuario.objects.get(username="usuarioTest")
        participaTest = Participa.objects.get(usuario=usuarioTest)

        Votacion.objects.create(nombre="test1", tiempo_votacion="01:15", participa=participaTest)
        Votacion.objects.create(nombre="", tiempo_votacion="01:15", participa=participaTest)
        Votacion.objects.create(nombre="test3", tiempo_votacion="00:00:59", participa=participaTest)

        test1 = Votacion.objects.get(nombre="test1")
        test2 = Votacion.objects.get(nombre="")
        test3 = Votacion.objects.get(nombre="test3")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "El nombre no puede estar vacío\n")
        self.assertEqual(test3.isOk(), "El tiempo mínimo es un minuto\n")

    def testVotacion_opcion(self):
        print("Realizando tests de opciones de votación")
        usuarioTest = Usuario.objects.get(username="usuarioTest")
        participaTest = Participa.objects.get(usuario=usuarioTest)
        votacionTest = Votacion(nombre="votacionTest", tiempo_votacion="01:15", participa=participaTest)
        votacionTest.save()

        Votacion_opcion.objects.create(nombre="test1", votacion=votacionTest)
        Votacion_opcion.objects.create(nombre="", votacion=votacionTest)

        test1 = Votacion_opcion.objects.get(nombre="test1")
        test2 = Votacion_opcion.objects.get(nombre="")

        self.assertEqual(test1.isOk(), "")
        self.assertEqual(test2.isOk(), "La opción de la votación no puede estar vacía\n")




