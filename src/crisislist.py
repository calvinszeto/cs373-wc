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
    def get(self):
        cris = Crisis.all()
        infos = Info.all()
        refs = Ref.all()
        cris_list = []
        for c in cris:
            index = len(cris_list)
            cris_list.append({"crisis":c})
            # Crisis - Info
            i = infos.ancestor(c).get()
            cris_list[index]["info"]=i
            # Crisis - Ref
            cris_list[index]["pimage"]=refs.ancestor(c).filter('ref_type =','primaryImage').get()
        template_values = {
            'crises':cris_list }
        path = os.path.join(os.path.dirname(__file__), '../templates/crisislist.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/crises', CrisisHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
