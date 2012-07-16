#!/usr/bin/env python
#

#
# goodbyeworld.py
# Handles the Export feature
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
        """
        Handles the export feature of the GAE application.
        Called at calvins-cs373-wc.appspot.com/export
        """
        self.response.headers.add_header('content-type','text/xml')

        crises = Crisis.all()
        assert(crises.get() is not None)
        orgs = Organization.all()
        assert(orgs.get() is not None)
        peeps = Person.all()
        assert(peeps.get() is not None)
        infos = Info.all()
        assert(infos.get() is not None)
        times = Time.all()
        assert(times.get() is not None)
        locs = Location.all()
        assert(locs.get() is not None)
        humans = Human.all()
        assert(humans.get() is not None)
        economics = Economic.all()
        assert(economics.get() is not None)
        contacts = Contact.all()
        assert(contacts.get() is not None)
        mails = Mail.all()
        assert(mails.get() is not None)
        refs = Ref.all()
        assert(refs.get() is not None)

        cris_list = []
        for c in crises:
            index = len(cris_list)
            cris_list.append({"crisis":c})
            # Crisis - Info
            i = infos.ancestor(c).get()
            cris_list[index]["info"]=i
            # Crisis - Info - Time
            cris_list[index]["time"]=times.ancestor(i).get()
            # Crisis - Info - Loc
            cris_list[index]["loc"]=locs.ancestor(i).get()
            # Crisis - Info - Impact - Human
            cris_list[index]["human"]=humans.ancestor(i).get()
            # Crisis - Info - Impact - Economic
            cris_list[index]["economic"]=economics.ancestor(i).get()
            # Crisis - Ref
            cris_list[index]["refs"]=refs.ancestor(c).run()
        org_list = []
        for o in orgs:
            index = len(org_list)
            org_list.append({"org":o})
            # Organization - Info
            i = infos.ancestor(c).get()
            org_list[index]["info"]=i
            """
            # Organization - Info - Contact
            con = contacts.ancestor(i).get()
            org_list[index]["contact"]=con
            # Organization - Info - Mail 
            org_list[index]["mail"]=mails.ancestor(con).get()
            """
            # Organization - Location
            org_list[index]["loc"]=locs.ancestor(i).get()
            # Organization - Ref
            org_list[index]["refs"]=refs.ancestor(o).run()
        persons_list = []
        for p in peeps:
            index = len(persons_list)
            persons_list.append({"person":p})
            # Person - Info
            i = infos.ancestor(p).get()
            persons_list[index]["info"]=i
            # Person - Info - Contact
            persons_list[index]["time"]=times.ancestor(i).get()
            # Person - Ref
            persons_list[index]["refs"]=refs.ancestor(p).run()
            
        template_values = {
            'crises':cris_list,
            'orgs':org_list,
            'persons':persons_list
            }
        path = os.path.join(os.path.dirname(__file__), 'template.xml')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication(
            [('/export', ExportHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
