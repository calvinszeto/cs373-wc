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
org_dict = {"name":"","misc":""}
org_info_dict = {"history":""}
org_contact_dict = {"phone":"","email":""}
org_loc_dict = {"city":"","region":"","country":""}
org_mail_dict = {"address":"","city":"","state":"","country":"","zip":""}
person_dict = {"name":"", "misc":""}
person_info_dict = {"nationality":"", "biography":""}
person_birth_dict = {"time":"","day":"","month":"","year":"","misc":""}

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
            for c in tree.findall("crisis"):
                for x in crisis_dict:
                    crisis_dict[x] = c.find(x).text
                cris = Crisis(**crisis_dict)
                cris.put()
                i = c.find("info")
                for x in info_dict:
                    info_dict[x] = i.find(x).text
                inf = Info(**info_dict)
                inf.info_help = i.find("help").text
                inf.info_type = i.find("type").text
                inf.put()
                t = i.find("time")
                for x in time_dict:
                    time_dict[x] = t.find(x).text
                tim = Time(**time_dict)
                tim.put()
                l = i.find("loc")
                for x in loc_dict:
                    loc_dict[x] = l.find(x).text
                loc = Location(**loc_dict)
                loc.put()
                h = i.find("impact/human")
                for x in human_dict:
                    human_dict[x] = h.find(x).text
                hum = Human(**human_dict)
                hum.put()
                e = i.find("impact/economic")
                for x in economic_dict:
                    economic_dict[x] = e.find(x).text
                eco = Economic(**economic_dict)
                eco.put()
                r = c.find("ref")
                pi = r.find("primaryImage")
                for x in ref_dict:
                    ref_dict[x] = pi.find(x).text
                pir = Ref(**ref_dict)
                pir.put()
                ii = r.find("image")
                for x in ref_dict:
                    ref_dict[x] = ii.find(x).text
                iir = Ref(**ref_dict)
                iir.put()
                vi = r.find("video")
                for x in ref_dict:
                    ref_dict[x] = vi.find(x).text
                vir = Ref(**ref_dict)
                vir.put()
                si = r.find("social")
                for x in ref_dict:
                    ref_dict[x] = si.find(x).text
                sir = Ref(**ref_dict)
                sir.put()
                ei = r.find("ext")
                for x in ref_dict:
                    ref_dict[x] = ei.find(x).text
                eir = Ref(**ref_dict)
                eir.put()
                    
                #organizations
                for o in tree.findall("organization"):
                    for x in org_dict:
                        org_dict[x] = c.find(x).text
                    org = Organization(**org_dict)
                    i = o.find("info")
                    for x in org_info_dict:
                        org_info_dict[x] = i.find(x).text
                    inf = Info(**org_info_dict)
                    inf.info_type = i.find("type").text
                    t = i.find("contact")
                    for x in org_contact_dict:
                        org_contact_dict[x] = t.find(x).text 
                    con = Contact(**org_contact_dict)	
                    l = i.find("loc")
                    for x in org_loc_dict:
                        org_loc_dict[x] = l.find(x).text
                    loc = Location(**org_loc_dict)
                    m = i.find("contact/mail")
                    for x in org_mail_dict:
                        org_mail_dict[x] = m.find(x).text
                    mail = Mail(**org_mail_dict)
                    r = c.find("ref")
                    pi = r.find("primaryImage")
                    for x in ref_dict:
                        ref_dict[x] = pi.find(x).text
                    pir = Ref(**ref_dict)
                    pir.put()
                    ii = r.find("image")
                    for x in ref_dict:
                        ref_dict[x] = ii.find(x).text
                    iir = Ref(**ref_dict)
                    iir.put()
                    vi = r.find("video")
                    for x in ref_dict:
                        ref_dict[x] = vi.find(x).text
                    vir = Ref(**ref_dict)
                    vir.put()
                    si = r.find("social")
                    for x in ref_dict:
                        ref_dict[x] = si.find(x).text
                    sir = Ref(**ref_dict)
                    sir.put()
                    ei = r.find("ext")
                    for x in ref_dict:
                        ref_dict[x] = ei.find(x).text
                    eir = Ref(**ref_dict)
                    eir.put()

                #person
                for p in tree.findall("person"):
                    for x in person_dict:
                        person_dict[x] = p.find(x).text
                    per = Person(**person_dict)
                    i = p.find("info")
                    for x in person_info_dict:
                        person_info_dict[x] = i.find(x).text
                    inf = Info(**person_info_dict)

                    inf.info_type = i.find("type").text
                    b = i.find("birthdate")
                    for x in person_birth_dict:
                        person_birth_dict[x] = b.find(x).text
                    bday = Time(**person_birth_dict)
                    r = c.find("ref")
                    pi = r.find("primaryImage")
                    for x in ref_dict:
                        ref_dict[x] = pi.find(x).text
                    pir = Ref(**ref_dict)
                    pir.put()
                    ii = r.find("image")
                    for x in ref_dict:
                        ref_dict[x] = ii.find(x).text
                    iir = Ref(**ref_dict)
                    iir.put()
                    vi = r.find("video")
                    for x in ref_dict:
                        ref_dict[x] = vi.find(x).text
                    vir = Ref(**ref_dict)
                    vir.put()
                    si = r.find("social")
                    for x in ref_dict:
                        ref_dict[x] = si.find(x).text
                    sir = Ref(**ref_dict)
                    sir.put()
                    ei = r.find("ext")
                    for x in ref_dict:
                        ref_dict[x] = ei.find(x).text
                    eir = Ref(**ref_dict)
                    eir.put()
        except AttributeError:
            print "Invalid"
        self.redirect("/", permanent=True)

def main():
    application = webapp.WSGIApplication(
            [('/import', MainHandler),
            ('/upload', UploadHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
