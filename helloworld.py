#!/usr/bin/env python
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


class StoredFiles(db.Model):
    nickname = db.StringProperty()
    blobkey = blobstore.BlobReferenceProperty()

    @staticmethod
    def get_all():
        query = db.Query(StoredFiles)
        files = query.get()

        return files


def doRender(handler, page, templatevalues=None):
    path = os.path.join(os.path.dirname(__file__), page)
    handler.response.out.write(template.render(path, templatevalues))

class MainHandler(webapp.RequestHandler):
    def get(self):

        cris = Crisis()
        cris.name = "Deepwater Horizon Oil Spill"
        print cris.name

        allfiles = StoredFiles.get_all()

        upload_url = blobstore.create_upload_url('/upload')

        templatevalues = {
                'allfiles': allfiles,
                'upload_url': upload_url,

            }
        doRender(self, 'index.html', templatevalues)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        newFile = StoredFiles()
        newFile.nickname = self.request.get('nickname')
        newFile.blobkey = blob_info.key()

        newFile.put()
        """
        while 1:
            line = br.readline()
            if not line:
                break
            print line
        """

        self.redirect('/')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

def main():
    application = webapp.WSGIApplication(
            [('/import', MainHandler),
            ('/upload', UploadHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

