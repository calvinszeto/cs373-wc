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
        cris = Crisis.all()
        orgs = Organization.all()
        people = Person.all()
        infos = Info.all()
        times = Time.all()
        humans = Human.all()
        ecos = Economic.all()
        refs = Ref.all()
        cris.filter('crisis_id =',crisisref)
        p = cris.get()
        crisis_list = {}
        crisis_list["crisis"]=p
        # crisis - Info
        i = infos.ancestor(p).get()
        crisis_list["info"]=i
        # crisis - Info - Contact
        crisis_list["time"]=times.ancestor(i).get()
        # crisis - Info - Impact - Human
        crisis_list["human"]=humans.ancestor(i).get()
        # crisis - Info - Impact - Human
        crisis_list["economic"]=ecos.ancestor(i).get()
        # crisis - Ref
        crisis_list["pimage"]=refs.ancestor(p).filter('ref_type =','primaryImage').get()
        refs = Ref.all()
        crisis_list["images"]=refs.ancestor(p).filter('ref_type =','image').run()
        refs = Ref.all()
        crisis_list["socials"]=refs.ancestor(p).filter('ref_type =','social').run()
        refs = Ref.all()
        crisis_list["videos"]=refs.ancestor(p).filter('ref_type =','video').run()
        refs = Ref.all()
        crisis_list["exts"]=refs.ancestor(p).filter('ref_type =','ext').run()
        refs = Ref.all()
        org = orgs.filter('org_id =',p.orgs[0]).get()
        crisis_list["org"]=org
        crisis_list["orgimage"]=refs.ancestor(org).filter('ref_type =','primaryImage').get()
        refs = Ref.all()
        per = people.filter('person_id =',p.persons[0]).get()
        crisis_list["person"]=per 
        crisis_list["personimage"]=refs.ancestor(per).filter('ref_type =','primaryImage').get()
        template_values = {
            'c':crisis_list }
        path = os.path.join(os.path.dirname(__file__), 'crisis.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/crisis/([^/]+)?', CrisisHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
