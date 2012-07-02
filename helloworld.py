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

crisis_dict = {"name":"","misc":""}
info_dict = {"history":"","resources":""}
time_dict = {"time":"","day":"","month":"","year":"","misc":""}
loc_dict = {"city":"","region":"","country":""}
human_dict = {"deaths":"","displaced":"","injured":"","missing":"","misc":""}
economic_dict = {"amount":"","currency":"","misc":""}
ref_dict = {"site":"","title":"","url":"","description":""}

class MainHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        try:
            print "Importing"
            # c = tree.find("crisis")
            for c in tree.findall("crisis"):
                for x in crisis_dict:
                    crisis_dict[x] = c.find(x).text
                cris = Crisis(**crisis_dict)
                i = c.find("info")
                for x in info_dict:
                    info_dict[x] = i.find(x).text
                inf = Info(**info_dict)
                inf.info_help = i.find("help").text
                inf.info_type = i.find("type").text
                t = i.find("time")
                for x in time_dict:
                    time_dict[x] = t.find(x).text
                tim = Time(**time_dict)
                l = i.find("loc")
                for x in loc_dict:
                    loc_dict[x] = l.find(x).text
                loc = Location(**loc_dict)
                h = i.find("impact/human")
                for x in human_dict:
                    human_dict[x] = h.find(x).text
                hum = Human(**human_dict)
                e = i.find("impact/economic")
                for x in economic_dict:
                    economic_dict[x] = e.find(x).text
                eco = Economic(**economic_dict)
                pi = Ref()
                ii = Ref()
                vi = Ref()
                si = Ref()
                ei = Ref()
                links = {"primaryImage":pi,"image":ii,"video":vi,"social":si,"ext":ei}
                r = c.find("ref")
                for z in links:
                    alk = r.find(z)
                    for x in ref_dict:
                        ref_dict[x] = alk.find(x).text
                    links[z] = Ref(**ref_dict)
                    
        except AttributeError:
            print "Invalid"
            

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

def main():
    application = webapp.WSGIApplication(
            [('/import', MainHandler),
            ('/upload', UploadHandler),
            ('/serve/([^/]+)?', ServeHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
