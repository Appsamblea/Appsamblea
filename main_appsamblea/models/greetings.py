# -*- encoding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def main_appsamblea_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    '''Constructs a Datastore key for a guestbook entity with main_appsamblea_name.'''
    return ndb.Key('guestbook', guestbook_name)

class Greeting(ndb.Model):
	'''Models an individual main_appsamblea entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

def GetEntityViaMemcache(entity_key):
	'''Get entity from memcache if available, from datastore if not.'''
	entity = memcache.get(str(entity_key))

	if entity is not None:
		return entity
  
	entity = entity_key.get()
	
	if entity is not None:
		memcache.set(str(entity_key), entity)

	return entity
