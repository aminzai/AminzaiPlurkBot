# Short URL Generator
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunwang --AT-- Gmail.com 
# Date      : Mon Oct  5 21:54:27 CST 2009
import urllib
import urllib2
import urlparse
import httplib
import random

class ShortURL:
  services = {
    'api.tr.im':   '/api/trim_simple?url=',
    'tinyurl.com': '/api-create.php?url=',
    'is.gd':       '/api.php?longurl='
  }
  def TrIm_query( self , url ):
    shortener = 'api.tr.im'
    c = httplib.HTTPConnection(shortener)
    c.request("GET", self.services[shortener] + urllib.quote(url))
    r = c.getresponse()
    shorturl = r.read().strip()
    if ("Error" not in shorturl) and ("http://" + urlparse.urlparse(shortener)[1] in shorturl):
      return shorturl
    else:
      raise IOError
  def TinyUrl_query( self , url ):
    shortener = 'tinyurl.com'
    c = httplib.HTTPConnection(shortener)
    c.request("GET", self.services[shortener] + urllib.quote(url))
    r = c.getresponse()
    shorturl = r.read().strip()
    if ("Error" not in shorturl) and ("http://" + urlparse.urlparse(shortener)[1] in shorturl):
      return shorturl
    else:
      raise IOError
  def IsGd_query( self , url ):
    shortener = 'is.gd'
    c = httplib.HTTPConnection(shortener)
    c.request("GET", self.services[shortener] + urllib.quote(url))
    r = c.getresponse()
    shorturl = r.read().strip()
    if ("Error" not in shorturl) and ("http://" + urlparse.urlparse(shortener)[1] in shorturl):
      return shorturl
    else:
      raise IOError
  def Randomi_Short_Url_Gen( self , url ):
    choice = [ 'TrIm' , 'TinyUrl' , 'IsGd' ] 
    rand = random.choice( choice ) 
    try:
      if rand == 'TrIm':
        return self.TrIm_query( url )
      elif rand == 'TinyUrl':
        return self.TinyUrl_query( url )
      elif rand == 'IsGd':
        return self.IsGd_query( url )
      else:
        return url
    except IOError:
        return url

if __name__ == '__main__' :
   print "Try to build short url & Random Choice"
   obj = ShortURL()
   while 1:
     a = raw_input("Please input url:")
     print obj.Randomi_Short_Url_Gen( a )
     #print obj.TrIm_query(a)
     #print obj.TinyUrl_query(a)
     #print obj.IsGd_query(a)
