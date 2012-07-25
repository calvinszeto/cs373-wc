#!/usr/bin/env python
#

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import urllib
from Models import *

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class PersonHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        personref = str(urllib.unquote(resource))
        peeps = Person.all()
        crises = Crisis.all()
        orgs = Organization.all()
        infos = Info.all()
        times = Time.all()
        refs = Ref.all()
        peeps.filter('person_id =',personref)
        p = peeps.get()
        persons_list = {}
        persons_list["person"]=p
        # Person - Info
        i = infos.ancestor(p).get()
        persons_list["info"]=i
        # Person - Info - Contact
        persons_list["time"]=times.ancestor(i).get()
        # Person - Ref
        persons_list["pimage"]=refs.ancestor(p).filter('ref_type =','primaryImage').get()
        refs = Ref.all()
        persons_list["images"]=refs.ancestor(p).filter('ref_type =','image').run()
        refs = Ref.all()
        persons_list["socials"]=refs.ancestor(p).filter('ref_type =','social').run()
        refs = Ref.all()
        persons_list["videos"]=refs.ancestor(p).filter('ref_type =','video').run()
        refs = Ref.all()
        persons_list["exts"]=refs.ancestor(p).filter('ref_type =','ext').run()
        refs = Ref.all()
        org = orgs.filter('org_id =',p.orgs[0]).get()
        persons_list["org"]=org
        persons_list["orgimage"]=refs.ancestor(org).filter('ref_type =','primaryImage').get()
        refs = Ref.all()
        cris = crises.filter('crisis_id =',p.crises[0]).get()
        persons_list["crisis"]=cris
        persons_list["crisisimage"]=refs.ancestor(cris).filter('ref_type =','primaryImage').get()
        template_values = {
            'persons':persons_list }
        path = os.path.join(os.path.dirname(__file__), '../templates/person.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/person/([^/]+)?', PersonHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()