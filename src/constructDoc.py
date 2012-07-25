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
        assert(infos.get() is not None)

        for c in crises:
            name = c.name
            i = infos.ancestor(c).get()
            content = i.history
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content))

        for o in orgs:
            name = o.name
            i = infos.ancestor(o).get()
            content = i.history
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content))

        for p in peeps:
            name = p.name
            i = infos.ancestor(p).get()
            content = i.biography
            search.Index(name=_INDEX_NAME).add(CreateDocument(name, content))

        self.redirect("/", permanent=True)

def CreateDocument(name, content):
    return search.Document(
        fields=[search.TextField(name='name', value=name),
                search.TextField(name='history', value=content)])

def main():
    application = webapp.WSGIApplication(
            [('/construct', ConstructHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
