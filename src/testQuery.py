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

class SearchHandler(webapp.RequestHandler):
    def get(self):
        """
        Handles the search feature of the GAE application.
        Called at calvins-cs373-wc.appspot.com/
        """
        """
        uri = urlparse(self.request.uri)
        query = ''
        if uri.query:
            query = parse_qs(uri.query)
            query = query['query'][0]
        query_obj = search.Query(query_string=query)
        """
        try:
            options = search.QueryOptions(
                #sort_options=sort,
                returned_fields=['name', 'history'],
                snippeted_fields=['history'])

            query = search.Query(query_string=self.request.get("q"), options=options)

            index = search.Index(name=_INDEX_NAME)

        # Execute the query
            results = index.search(query)

            for scored_document in results:
                #self.response.out.write(scored_document.fields[0].value)
                for fields in scored_document.fields:
                    self.response.out.write(fields.value)

            #results = search.Index(name=_INDEX_NAME).search(query=self.request.get("q"))
            #self.response.out.write(index.search(query))
        except search.Error:
            logging.exception('Search failed')

def main():
    application = webapp.WSGIApplication(
            [('/search', SearchHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
