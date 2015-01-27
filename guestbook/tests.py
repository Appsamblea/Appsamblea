# -*- encoding: utf-8 -*-
import django.core.handlers.wsgi
import webtest
from datetime import time
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
from django.utils import timezone
from guestbook.models import *

class GuestBookViewsTestCase(django.test.TestCase):
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

		fechaTest = timezone.make_aware("2015-01-01", timezone.get_current_timezone())

		#Usuario común
		usuario_test = Usuario(password="", nombre="usuarioTest", apellidos="", fecha_nac=fechaTest, telefono="", email="", localidad="", pais="", bio="")
		usuario_test.save()

		#Organización común
		organizacion_test = Organizacion(nombre="organizacionTest", tematica="A")
		organizacion_test.save()

		#Asamblea común
		asamblea_test = Asamblea(nombre = "asambleaTest", fecha = fechaTest, descripcion = "Asamblea de prueba", usuario = usuario_test, organizacion = organizacion_test)
		asamblea_test.save()

	#def tearDown(self):
	def tearDown(self):
		usuario_test = Usuario.objects.get(nombre = "usuarioTest")
		organizacion_test = Organizacion.objects.get(nombre = "organizacionTest")
		usuario_test.delete()
		organizacion_test.delete()
		self.testbed.deactivate()

	'''
	def test_index(self):
		response = self.testapp.get('/guestbook/')
		self.assertEqual(response.status_int, 200)

	def test_sign(self):
		response = self.testapp.get('/guestbook/sign/')
		self.assertEqual(response.status_int, 302)	
	

	def testInsertEntity(self):
		greeting_test = Greeting(content = "Testing", parent = guestbook_key(DEFAULT_GUESTBOOK_NAME))
		greeting_test.put()
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME))

		self.assertEqual(1, len(greetings_query.fetch(2)))

	def testFilterByUser(self):
		anonymous_user = users.User(email="anonymous@testing.com")
		test_user = users.User(email="test@testing.com")
		Greeting(content = "Testing", parent = guestbook_key(DEFAULT_GUESTBOOK_NAME), author = anonymous_user).put()
		Greeting(content = "Testing2", parent = guestbook_key(DEFAULT_GUESTBOOK_NAME), author = test_user).put()
		greetings_query = Greeting.query(ancestor=guestbook_key(DEFAULT_GUESTBOOK_NAME)).filter(ndb.GenericProperty('author') == anonymous_user)
		results = greetings_query.fetch(2)
		self.assertEqual(1, len(results))
		self.assertEqual(anonymous_user, results[0].author)

	def testGetEntityViaMemcache(self):
		entity_key = Greeting(content = "Testing", parent = guestbook_key(DEFAULT_GUESTBOOK_NAME)).put()
		retrieved_entity = GetEntityViaMemcache(entity_key)
		self.assertNotEqual(None, retrieved_entity)
		self.assertEqual("Testing", retrieved_entity.content
	'''

	def testActas(self):
		asamblea_test = Asamblea.objects.get(nombre = "asambleaTest")

		Acta.objects.create(texto = "Asamblea de prueba", asamblea = asamblea_test)
		Acta.objects.create(texto = "", asamblea = asamblea_test)

		test1 = Acta.objects.get(texto = "Asamblea de prueba")
		test2 = Acta.objects.get(texto = "")

		self.assertEqual(test1.isOk(), "")
		self.assertEqual(test2.isOk(), "El texto está vacío\n")



	def testAsambleas(self):
		usuario_test = Usuario.objects.get(nombre = "usuarioTest")
		organizacion_test = Organizacion.objects.get(nombre = "organizacionTest")

		Asamblea.objects.create(nombre="test1", fecha="2013-02-28", descripcion=" ", usuario_id=usuario_test.id, organizacion=organizacion_test, es_abierta = True)
		Asamblea.objects.create(nombre="", fecha="2013-02-28", descripcion="asdasd", usuario_id=usuario_test.id, organizacion=organizacion_test, es_abierta = True)
		Asamblea.objects.create(nombre="test3", fecha="2013-12-13", descripcion="asamblea de prueba", usuario_id=usuario_test.id, organizacion=organizacion_test, url_streaming = "http://www.google.es")
		Asamblea.objects.create(nombre="test4", fecha="2013-12-13", descripcion="asamblea de prueba", usuario_id=usuario_test.id, organizacion=organizacion_test, url_streaming = "www.aiurhtaiurutiaert.es")
		Asamblea.objects.create(nombre="test5", fecha="2013-12-13", descripcion="asamblea de prueba", usuario_id=usuario_test.id, organizacion=organizacion_test, urlasamblea = "http://www.google.es")
		Asamblea.objects.create(nombre="test6", fecha="2013-12-13", descripcion="asamblea de prueba", usuario_id=usuario_test.id, organizacion=organizacion_test, urlasamblea = "www.aiurhtaiurutiaert.es")

		test1 = Asamblea.objects.get(nombre = "test1")
		test2 = Asamblea.objects.get(descripcion = "asdasd")
		test3 = Asamblea.objects.get(nombre = "test3")
		test4 = Asamblea.objects.get(nombre = "test4")
		test5 = Asamblea.objects.get(nombre = "test5")
		test6 = Asamblea.objects.get(nombre = "test6")

		self.assertEqual(test1.isOk(), "La descripción debe de estar vacía\n")
		self.assertEqual(test2.isOk(), "El nombre está vacío\n")		
		self.assertEqual(test3.isOk(), "")		
		self.assertEqual(test4.isOk(), "La URL del streaming no funciona\n")
		self.assertEqual(test5.isOk(), "")		
		self.assertEqual(test6.isOk(), "La URL de la asamblea no funciona\n")

	def testOrganizaciones(self):
		organizacion_test1 = Organizacion.objects.create(nombre="test1", tematica="tematica", descripcion="asdasdasd", email="ererererr@asd.com", web="http://www.google.es")
		Organizacion.objects.create(nombre="", tematica="tematica", descripcion="test2", email="ererererr@asd.com", web="http://www.google.es")
		Organizacion.objects.create(nombre="test3", tematica="", descripcion="asdasdasd", email="ererererr@asd.com", web="http://www.google.es")
		Organizacion.objects.create(nombre="test4", tematica="tematica", descripcion="", email="ererererr@asd.com", web="http://www.google.es")
		Organizacion.objects.create(nombre="test5", tematica="tematica", descripcion="asdasdasd", email="ererererr@asd.com", web="www.iakjrtlajrtoiaer.es")
		
		test1 = Organizacion.objects.get(nombre = "test1")
		test2 = Organizacion.objects.get(descripcion = "test2")
		test3 = Organizacion.objects.get(nombre = "test3")
		test4 = Organizacion.objects.get(nombre = "test4")
		test5 = Organizacion.objects.get(nombre = "test5")

		self.assertEqual(test1.isOk(), "")
		self.assertEqual(test2.isOk(), "El nombre está vacío\n")
		self.assertEqual(test3.isOk(), "La temática está vacía\n")
		self.assertEqual(test4.isOk(), "La descripción está vacía\n")
		self.assertEqual(test5.isOk(), "La URL de la organización no funciona\n")
