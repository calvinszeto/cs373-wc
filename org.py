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
    def get(self, resource):
        orgref = str(urllib.unquote(resource))
        o = Organization.all()
        infos = Info.all()
        contact = Contact.all()
        mail = Mail.all()
        refs = Ref.all()
        o.filter('org_id =',orgref)
        p = o.get()
        org_list = {}
        org_list["organization"]=p
        # organization - Info
        i = infos.ancestor(p).get()
        org_list["info"]=i
        # organization - Info - Contact
        co = contact.ancestor(i).get()
        org_list["contact"] = co
        #organization - Info - Contact - mail
        m = mail.ancestor(i).get()
        org_list["mail"] = m
        # organization - Ref
        org_list["pimage"]=refs.ancestor(p).filter('ref_type =','primaryImage').get()
        refs = Ref.all()
        org_list["images"]=refs.ancestor(p).filter('ref_type =','image').run()
        refs = Ref.all()
        org_list["socials"]=refs.ancestor(p).filter('ref_type =','social').run()
        refs = Ref.all()
        org_list["videos"]=refs.ancestor(p).filter('ref_type =','video').run()
        refs = Ref.all()
        org_list["exts"]=refs.ancestor(p).filter('ref_type =','ext').run()
        template_values = {
            'o':org_list }
        path = os.path.join(os.path.dirname(__file__), 'org.html')
        self.response.out.write(template.render(path, template_values))
         

def main():
    application = webapp.WSGIApplication(
            [('/org/([^/]+)?', OrgHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()