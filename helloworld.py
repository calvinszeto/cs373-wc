#!/usr/bin/env python
#

import os
import urllib

from xml.etree.ElementTree import ElementTree
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


class Crisis(db.Model):
    idstring = db.StringProperty()
    name = db.StringProperty()
    info_history = db.StringProperty()
    info_help = db.StringProperty()
    info_resources = db.StringProperty()
    info_type = db.StringProperty()
    info_time_time= db.StringProperty()
    info_time_day = db.StringProperty()
    info_time_month = db.StringProperty()
    info_time_year = db.StringProperty()
    info_time_misc = db.StringProperty()
    info_loc_city = db.StringProperty()
    info_loc_region = db.StringProperty()
    info_loc_country = db.StringProperty()
    info_impact_human_deaths = db.StringProperty()
    info_impact_human_displaced = db.StringProperty()
    info_impact_human_injured = db.StringProperty()
    info_impact_human_missing = db.StringProperty()
    info_impact_human_misc = db.StringProperty()
    info_impact_economic_amount = db.StringProperty()
    info_impact_economic_currency = db.StringProperty()
    info_impact_economic_misc = db.StringProperty()
    ref_image_title = db.StringProperty()
    ref_image_url = db.StringProperty()
    ref_image_description = db.StringProperty()
    ref_video_site = db.StringProperty()
    ref_video_title = db.StringProperty()
    ref_video_url = db.StringProperty()
    ref_video_description = db.StringProperty()
    ref_social_title = db.StringProperty()
    ref_social_url = db.StringProperty()
    ref_ext_title = db.StringProperty()
    ref_ext_url = db.StringProperty()
    ref_ext_description = db.StringProperty()
    misc = db.StringProperty()
    orgidref = db.StringProperty()
    personidref = db.StringProperty()

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
        br = blob_info.open()
        """
        while 1:
            line = br.readline()
            if not line:
                break
            print line
        """
        tree = ElementTree()
        tree.parse(br)
        cdict = {name:"crisis/name"}
        c = Crisis()
        for y in cdict:
            c.y
        # c.name = tree.find("crisis/name").text
        print c.name
        c.put()

        #self.redirect('/')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

def main():
    application = webapp.WSGIApplication(
            [('/', MainHandler),
            ('/upload', UploadHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

