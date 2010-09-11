from google.appengine.ext import db
from google.appengine.api import datastore_types
from django.utils import simplejson

class DictProperty(db.Property):

    data_type=datastore_types.Text

    def get_value_for_datastore(self,model):
        value = super(DictProperty,self).get_value_for_datastore(model)
        return self._deflate(value)

    def validate(self,value):
        return self.make_value_from_datastore(value)

    def make_value_from_datastore(self, value):
        return self._inflate(value)

    def _inflate(self, value):
        if value is None:
            return {}
        if isinstance(value, unicode) or isinstance(value ,str ):
            return simplejson.loads(value)
        return value

    def _deflate(self,value):
        return simplejson.dumps(value)


class RssResource(db.Model):
    """
    Recore the rss resource
    """
    name = db.StringProperty()
    url = db.StringProperty()

class WaitPost(db.Model):
    """
    It's a queue to record rss information
    """
    desc = db.StringProperty()
    link = db.StringProperty()
    res = db.ReferenceProperty(reference_class = RssResource , collection_name='resource')
