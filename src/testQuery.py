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

def CreateDocument(did, name, content, idref):
    return search.Document(
        doc_id = did,
        fields=[search.TextField(name='name', value=name),
                search.TextField(name='history', value=content),
                search.TextField(name='idref', value=idref)])

class SearchHandler(webapp.RequestHandler):
    def construct(self):
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

        counter = 0
        for c in crises:
            name = c.name
            i = infos.ancestor(c).get()
            content = i.history
            idref = c.crisis_id
            search.Index(name=_INDEX_NAME).add(CreateDocument("crisis"+str(counter), name, content, idref))
            counter += 1
        counter = 0
        for o in orgs:
            name = o.name
            i = infos.ancestor(o).get()
            content = i.history
            idref = o.org_id
            search.Index(name=_INDEX_NAME).add(CreateDocument("org"+str(counter), name, content, idref))
            counter += 1
        
        counter = 0
        for p in peeps:
            name = p.name
            i = infos.ancestor(p).get()
            content = i.biography
            idref = p.person_id
            search.Index(name=_INDEX_NAME).add(CreateDocument("person"+str(counter), name, content, idref))
            counter += 1

    def get(self):
        """
        Handles the search feature of the GAE application.
        Called at calvins-cs373-wc.appspot.com/
        """
        try:
            self.construct()
            options = search.QueryOptions(
                returned_fields=['name', 'history', 'idref'],
                snippeted_fields=['history'])
            query = search.Query(query_string=self.request.get("q"), options=options)
            index = search.Index(name=_INDEX_NAME)

            # Execute the query
            results = index.search(query)

            result_list = [] 
            refs = Ref.all()

            for scored_document in results:
                index = len(result_list)
                result_list.append({}) 
                doc_type = " "
                id_ref = " "
                # self.response.out.write(scored_document.fields[0].value)
                for fields in scored_document.fields:
                    if fields.name == "idref":
                        id_ref = fields.value
                    else:
                        result_list[index][fields.name] = fields.value
                    # self.response.out.write(str(fields.value) + " ")
                ref = None
                if "crisis" in scored_document.doc_id:
                    doc_type = "crisis"
                    ref = refs.ancestor(Crisis.all().filter('crisis_id =',id_ref).get()).filter('ref_type =', 'primaryImage').get()
                if "org" in scored_document.doc_id:
                    ref = refs.ancestor(Organization.all().filter('org_id =',id_ref).get()).filter('ref_type =', 'primaryImage').get()
                    doc_type = "org"
                if "person" in scored_document.doc_id:
                    ref = refs.ancestor(Person.all().filter('person_id =',id_ref).get()).filter('ref_type =', 'primaryImage').get()
                    doc_type = "person"
                result_list[index]["image"] = ref.url
                link = "/%s/%s" % (doc_type,id_ref)
                # self.response.out.write(link)
                result_list[index]["link"] = link
                
            template_values = {
                    'results':result_list
                }
            path = os.path.join(os.path.dirname(__file__), '../templates/searchresults.html')
            self.response.out.write(template.render(path, template_values))
        except search.Error:
            logging.exception('Search failed')

def main():
    application = webapp.WSGIApplication(
            [('/search', SearchHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
