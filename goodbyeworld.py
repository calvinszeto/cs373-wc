#!/usr/bin/env python
#

import os
import urllib
from Models import *

from xml.etree.ElementTree import ElementTree
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class ExportHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header('content-type','text/xml')
        self.response.out.write("""<worldCrises>\n""")
        crises = Crisis.all()
        for c in crises:
            infos = query(type is info and parent is c)
            infos.history
            self.response.out.write("""<crisis>
                                        <name>%s</name>
                                        </crisis>""" % c.name)
        self.response.out.write("""</worldCrises>""")

def main():
    application = webapp.WSGIApplication(
            [('/export', ExportHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
