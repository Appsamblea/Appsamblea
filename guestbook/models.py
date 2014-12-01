'''
Created on 25/11/2014

@author: silt
'''
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
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
