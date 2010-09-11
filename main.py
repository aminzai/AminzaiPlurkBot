#!/usr/bin/env python2.5
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required

import feedparser
import model

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class GetRssInf(webapp.RequestHandler):
    """
    User this to  test get rss resource

    """
    def get(self):
        d = feedparser.parse("http://feeds.feedburner.com/isu")
        for x in d['entries']:
            self.response.out.write(x['title']+"<br />")
            self.response.out.write(x['link']+"<br />")

class GetRss(webapp.RequestHandler):
    """
    """

class InitSystem(webapp.RequestHandler):
    """
    Init the system
    """
    @login_required
    def get(self):
        if users.is_current_user_admin():
            d = model.RssResource(
                name = 'ISU',
                url = 'http://feeds.feedburner.com/isu'
            ).put()
        else:
            self.response.out.write("You're not admin user sorry!!")

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                         ('/gri',GetRssInf),
                                         ('/init',InitSystem)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
