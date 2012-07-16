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

class PersonHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        peeps = Person.all()
        infos = Info.all()
        refs = Ref.all()
        persons_list = []
        for p in peeps:
            index = len(persons_list)
            persons_list.append({"person":p})
            # Person - Info
            i = infos.ancestor(p).get()
            persons_list[index]["info"]=i
            # Person - Ref
            persons_list[index]["pimage"]=refs.ancestor(p).filter('ref_type =','primaryImage').get()
        template_values = {
            'persons':persons_list }
        path = os.path.join(os.path.dirname(__file__), 'personlist.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/people', PersonHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
