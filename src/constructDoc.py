#!/usr/bin/env python
#

#
# goodbyeworld.py
# Handles the Export feature
#

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import urllib
from Models import *

from xml.etree.ElementTree import ElementTree
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from cgi import parse_qs
import os
import string
import urllib
from urlparse import urlparse

from google.appengine.api import search
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

_INDEX_NAME = 'cry'

class ConstructHandler(webapp.RequestHandler):
    def get(self):
        doc_index = search.Index(name=_INDEX_NAME)

        while True:
            document_ids = [document.doc_id for document in doc_index.list_documents(ids_only=True)]
            if not document_ids:
                break
            doc_index.remove(document_ids)
        crises = Crisis.all()
        assert(crises.get() is not None)
        orgs = Organization.all()
        peeps = Person.all()
        infos = Info.all()
        ref = Ref.all()
        assert(infos.get() is not None)

        cris_list = []
	"""        
	for c in crises:
            index = len(cris_list)
            cris_list.append({"crisis":c})
            name = c.name
            cris_list[index]["name"]=name
            # Crisis - Info
            i = infos.ancestor(c).get()
            cris_list[index]["content"]=i
            content = i.history
            # Crisis - Ref
            r = ref.ancestor(c).filter('ref_type =','primaryImage').get()
            cris_list[index]["pimage"]=r
            pimage = r.url
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content, pimage))
	"""
        counter = 0
	for c in crises:
            name = c.name
            i = infos.ancestor(c).get()
            content = i.history
            idref = c.crisis_id
            #c_list[index]["pimage"]=refs.ancestor(o).filter('ref_type =','primaryImage').get()
	    #refs = o_list[index]["pimage"]
            
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content, idref))
            ++counter

	
        for o in orgs:
            name = o.name
            i = infos.ancestor(o).get()
            content = i.history
            idref = o.org_id
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content, idref))
        
        for p in peeps:
            name = p.name
            i = infos.ancestor(p).get()
            content = i.biography
            idref = p.person_id
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content, idref))
	"""
	template_values = {
            'crisis' : cris_list}

	self.response.out.write(template.render(path, template_values))
	"""
        self.redirect("/", permanent=True)

def CreateDocument(name, content, idref):
    return search.Document(
        fields=[search.TextField(name='name', value=name),
                search.TextField(name='history', value=content),
                search.TextField(name='idref', value=idref)])

def main():
    application = webapp.WSGIApplication(
            [('/construct', ConstructHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
