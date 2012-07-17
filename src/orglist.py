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

class OrgHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        orgs = Organization.all()
        infos = Info.all()
        refs = Ref.all()
        org_list = []
        for o in orgs:
            index = len(org_list)
            org_list.append({"org":o})
            # Organization - Info
            i = infos.ancestor(o).get()
            org_list[index]["info"]=i
            # Organization - Ref
            org_list[index]["pimage"]=refs.ancestor(o).filter('ref_type =','primaryImage').get()
        template_values = {
            'orgs':org_list
            }
        path = os.path.join(os.path.dirname(__file__), '../templates/orglist.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/orgs', OrgHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
