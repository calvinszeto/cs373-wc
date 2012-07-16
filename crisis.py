#!/usr/bin/env python
#

import os
import urllib
from Models import *

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class CrisisHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        crisisref = str(urllib.unquote(resource))
        crises = Crisis.all()
        crises.filter('crisis_id =',crisisref)
        c = crises.get()
        print c.name
        # path = os.path.join(os.path.dirname(__file__), 'crisis.html')
        # self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/crisis/([^/]+)?', CrisisHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
