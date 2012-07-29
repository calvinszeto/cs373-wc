#!/usr/bin/env python
#

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import urllib
from Models import *

from xml.etree.ElementTree import ElementTree
from google.appengine.api import taskqueue
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
org_dict = {"name":"","misc":""}
org_info_dict = {"history":""}
org_contact_dict = {"phone":"","email":""}
org_loc_dict = {"city":"","region":"","country":""}
org_mail_dict = {"address":"","city":"","state":"","country":"","zip":""}
person_dict = {"name":"", "misc":""}
person_info_dict = {"nationality":"", "biography":""}
person_birth_dict = {"time":"","day":"","month":"","year":"","misc":""}

class ValidateHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        """
        Validates the given XML
        """
        try:
            upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
            blob_info = upload_files[0]
            br = blob_info.open()
            tree = ElementTree()
            tree.parse(br)
            # Crises
            for c in tree.findall("crisis"):
                for x in crisis_dict:
                    text = c.find(x).text
                text = c.attrib["id"]
                # Crisis - Org
                for org in c.findall("org"):
                    text = org.attrib["idref"] 
                # Crisis - Person
                for person in c.findall("person"):
                    text = person.attrib["idref"] 
                # Crisis - Info
                i = c.find("info")
                for x in info_dict:
                    text = i.find(x).text
                text = i.find("help").text
                text = i.find("type").text
                # Crisis - Info - Time
                t = i.find("time")
                for x in time_dict:
                    text = t.find(x).text
                # Crisis - Info - Location
                l = i.find("loc")
                for x in loc_dict:
                    text = l.find(x).text
                # Crisis - Info - Impact/Human
                h = i.find("impact/human")
                for x in human_dict:
                    text = h.find(x).text
                # Crisis - Info - Impact/Economic
                e = i.find("impact/economic")
                for x in economic_dict:
                    text = e.find(x).text
                # Crisis - Ref
                r = c.find("ref")
                for pi in r.findall("primaryImage"):
                    for x in ref_dict:
                        text = pi.find(x).text
                for ii in r.findall("image"):
                    for x in ref_dict:
                        text = ii.find(x).text
                for vi in r.findall("video"):
                    for x in ref_dict:
                        text = vi.find(x).text
                for si in r.findall("social"):
                    for x in ref_dict:
                        text = si.find(x).text
                for ei in r.findall("ext"):
                    for x in ref_dict:
                        text = ei.find(x).text
            
            # Organizations
            for o in tree.findall("organization"):
                for x in org_dict:
                    text = c.find(x).text
                text = o.attrib["id"]
                # Organization - Org
                for cris in o.findall("crisis"):
                    text=cris.attrib["idref"] 
                # Organization - Person
                for person in o.findall("person"):
                    text=person.attrib["idref"] 
                # Organization - Info
                i = o.find("info")
                for x in org_info_dict:
                    text = i.find(x).text
                text = i.find("type").text
                # Organization - Info - Contact
                t = i.find("contact")
                for x in org_contact_dict:
                    text = t.find(x).text 
                # Organization - Info - Contact - Mail
                m = i.find("contact/mail")
                for x in org_mail_dict:
                    text = m.find(x).text
                # Organization - Info - Location
                l = i.find("loc")
                for x in org_loc_dict:
                    text = l.find(x).text
                # Organization - Ref
                r = o.find("ref")
                for pi in r.findall("primaryImage"):
                    for x in ref_dict:
                        text = pi.find(x).text
                for ii in r.findall("image"):
                    for x in ref_dict:
                        text = ii.find(x).text
                for vi in r.findall("video"):
                    for x in ref_dict:
                        text = vi.find(x).text
                for si in r.findall("social"):
                    for x in ref_dict:
                        text = si.find(x).text
                for ei in r.findall("ext"):
                    for x in ref_dict:
                        text = ei.find(x).text

            # Person
            for p in tree.findall("person"):
                for x in person_dict:
                    text = p.find(x).text
                text = p.attrib["id"]
                # Person - Crisis
                for cris in p.findall("crisis"):
                    text=cris.attrib["idref"]
                # Person - Org
                for org in p.findall("org"):
                    text=org.attrib["idref"] 
                # Person - Info
                i = p.find("info")
                for x in person_info_dict:
                    text = i.find(x).text
                text = i.find("type").text
                # Person - Info - Birthdate
                b = i.find("birthdate")
                for x in person_birth_dict:
                    text = b.find(x).text
                # Person - Ref
                r = p.find("ref")
                for pi in r.findall("primaryImage"):
                    for x in ref_dict:
                        text = pi.find(x).text
                for ii in r.findall("image"):
                    for x in ref_dict:
                        text = ii.find(x).text
                for vi in r.findall("video"):
                    for x in ref_dict:
                        text = vi.find(x).text
                for si in r.findall("social"):
                    for x in ref_dict:
                        text = si.find(x).text
                for ei in r.findall("ext"):
                    for x in ref_dict:
                        text = ei.find(x).text
                self.redirect('/mergeserve/%s' % blob_info.key())
        except :
            self.response.out.write("Invalid XML")

def main():
    application = webapp.WSGIApplication(
            [('/validate', ValidateHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
