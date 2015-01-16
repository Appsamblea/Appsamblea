import unittest
import django.core.handlers.wsgi
import webtest
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
from guestbook.models import Greeting, guestbook_key, GetEntityViaMemcache, DEFAULT_GUESTBOOK_NAME

class GuestBookViewsTestCase(unittest.TestCase):
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

		#Asambleas
		Asamblea(nombre="test1", fecha="21/13/2013", descripcion="asamblea de prueba")

 	 
	def tearDown(self):
		self.testbed.deactivate()

	'''
	def test_index(self):
		response = self.testapp.get('/guestbook/')
		self.assertEqual(response.status_int, 200)

	def test_sign(self):
		response = self.testapp.get('/guestbook/sign/')
		self.assertEqual(response.status_int, 302)	
	'''

	def testInsertEntity(self):
		Greeting(content = "Testing", parent = guestbook_key(DEFAULT_GUESTBOOK_NAME)).put()
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
		self.assertEqual("Testing", retrieved_entity.content)

	def testAsambleas(self):
		test = get(nombre="test1")
		self.assertEqual(test.isOk())
