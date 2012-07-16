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
        """
        Handles the import feature by posting the HTML which accepts a file.
        Then file is stored as a blob and UploadHandler is called.
        """
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def validate(self):
        """
        Validates the given XML
        """
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        br = blob_info.open()
        tree = ElementTree()
        tree.parse(br)
        try:
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
        except :
            self.response.out.write("Invalid XML")
            return False
        return True

    def post(self):
        """
        Handles the import of a file into the GAE Models.
        Searches for specific tags per the Schema and quits if file is invalid.
        """
        if(not self.validate()):
            return
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        db.delete(db.Query(keys_only=True)) # Clear the datastore
        assert(Crisis.all().get() is None)
        # Crises
        for c in tree.findall("crisis"):
            for x in crisis_dict:
                text = c.find(x).text
                crisis_dict[x] = text if text is not None else ""
            cris = Crisis(**crisis_dict)
            cris.crisis_id = c.attrib["id"]
            # Crisis - Org
            for org in c.findall("org"):
                cris.orgs.append(org.attrib["idref"]) 
            # Crisis - Person
            for person in c.findall("person"):
                cris.persons.append(person.attrib["idref"]) 
            cris.put()
            # Crisis - Info
            i = c.find("info")
            for x in info_dict:
                text = i.find(x).text
                info_dict[x] = text if text is not None else ""
            inf = Info(parent=cris,**info_dict)
            inf.info_help = i.find("help").text
            inf.info_type = i.find("type").text
            inf.put()
            # Crisis - Info - Time
            t = i.find("time")
            for x in time_dict:
                text = t.find(x).text
                time_dict[x] = text if text is not None else ""
            tim = Time(parent=inf,**time_dict)
            tim.put()
            # Crisis - Info - Location
            l = i.find("loc")
            for x in loc_dict:
                text = l.find(x).text
                loc_dict[x] = text if text is not None else ""
            loc = Location(parent=inf,**loc_dict)
            loc.put()
            # Crisis - Info - Impact/Human
            h = i.find("impact/human")
            for x in human_dict:
                text = h.find(x).text
                human_dict[x] = text if text is not None else ""
            hum = Human(parent=inf,**human_dict)
            hum.put()
            # Crisis - Info - Impact/Economic
            e = i.find("impact/economic")
            for x in economic_dict:
                text = e.find(x).text
                economic_dict[x] = text if text is not None else ""
            eco = Economic(parent=inf,**economic_dict)
            eco.put()
            # Crisis - Ref
            r = c.find("ref")
            for pi in r.findall("primaryImage"):
                for x in ref_dict:
                    text = pi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                pir = Ref(parent=cris,**ref_dict)
                pir.ref_type="primaryImage"
                pir.put()
            for ii in r.findall("image"):
                for x in ref_dict:
                    text = ii.find(x).text
                    ref_dict[x] = text if text is not None else ""
                iir = Ref(parent=cris,**ref_dict)
                iir.ref_type="image"
                iir.put()
            for vi in r.findall("video"):
                for x in ref_dict:
                    text = vi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                vir = Ref(parent=cris,**ref_dict)
                vir.ref_type="video"
                vir.put()
            for si in r.findall("social"):
                for x in ref_dict:
                    text = si.find(x).text
                    ref_dict[x] = text if text is not None else ""
                sir = Ref(parent=cris,**ref_dict)
                sir.ref_type="social"
                sir.put()
            for ei in r.findall("ext"):
                for x in ref_dict:
                    text = ei.find(x).text
                    ref_dict[x] = text if text is not None else ""
                eir = Ref(parent=cris,**ref_dict)
                eir.ref_type="ext"
                eir.put()
        assert(Crisis.all().get() is not None) 
        # Organizations
        for o in tree.findall("organization"):
            for x in org_dict:
                text = c.find(x).text
                org_dict[x] = text if text is not None else ""
            org = Organization(**org_dict)
            org.org_id = o.attrib["id"]
            # Organization - Org
            for cris in o.findall("crisis"):
                org.crises.append(cris.attrib["idref"]) 
            # Organization - Person
            for person in o.findall("person"):
                org.persons.append(person.attrib["idref"]) 
            org.put()
            # Organization - Info
            i = o.find("info")
            for x in org_info_dict:
                text = i.find(x).text
                org_info_dict[x] = text if text is not None else ""
            inf = Info(parent=org,**org_info_dict)
            inf.info_type = i.find("type").text
            inf.put()
            # Organization - Info - Contact
            t = i.find("contact")
            for x in org_contact_dict:
                text = t.find(x).text 
                org_contact_dict[x] = text if text is not None else ""
            con = Contact(parent=inf,**org_contact_dict)	
            con.put()
            # Organization - Info - Contact - Mail
            m = i.find("contact/mail")
            for x in org_mail_dict:
                text = m.find(x).text
                org_mail_dict[x] = text if text is not None else ""
            mail = Mail(parent=con,**org_mail_dict)
            mail.put()
            # Organization - Info - Location
            l = i.find("loc")
            for x in org_loc_dict:
                text = l.find(x).text
                org_loc_dict[x] = text if text is not None else ""
            loc = Location(parent=inf,**org_loc_dict)
            loc.put()
            # Organization - Ref
            r = o.find("ref")
            for pi in r.findall("primaryImage"):
                for x in ref_dict:
                    text = pi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                pir = Ref(parent=org,**ref_dict)
                pir.ref_type="primaryImage"
                pir.put()
            for ii in r.findall("image"):
                for x in ref_dict:
                    text = ii.find(x).text
                    ref_dict[x] = text if text is not None else ""
                iir = Ref(parent=org,**ref_dict)
                iir.ref_type="image"
                iir.put()
            for vi in r.findall("video"):
                for x in ref_dict:
                    text = vi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                vir = Ref(parent=org,**ref_dict)
                vir.ref_type="video"
                vir.put()
            for si in r.findall("social"):
                for x in ref_dict:
                    text = si.find(x).text
                    ref_dict[x] = text if text is not None else ""
                sir = Ref(parent=org,**ref_dict)
                sir.ref_type="social"
                sir.put()
            for ei in r.findall("ext"):
                for x in ref_dict:
                    text = ei.find(x).text
                    ref_dict[x] = text if text is not None else ""
                eir = Ref(parent=org,**ref_dict)
                eir.ref_type="ext"
                eir.put()
        assert(Organization.all().get() is not None) 

        # Person
        for p in tree.findall("person"):
            for x in person_dict:
                text = p.find(x).text
                person_dict[x] = text if text is not None else ""
            per = Person(**person_dict)
            per.person_id = p.attrib["id"]
            # Person - Crisis
            for cris in p.findall("crisis"):
                per.crises.append(cris.attrib["idref"]) 
            # Person - Org
            for org in p.findall("org"):
                per.orgs.append(org.attrib["idref"]) 
            per.put()
            # Person - Info
            i = p.find("info")
            for x in person_info_dict:
                text = i.find(x).text
                person_info_dict[x] = text if text is not None else ""
            inf = Info(parent=per,**person_info_dict)
            inf.info_type = i.find("type").text
            inf.put()
            # Person - Info - Birthdate
            b = i.find("birthdate")
            for x in person_birth_dict:
                text = b.find(x).text
                person_birth_dict[x] = text if text is not None else ""
            bday = Time(parent=inf,**person_birth_dict)
            bday.put()
            # Person - Ref
            r = p.find("ref")
            for pi in r.findall("primaryImage"):
                for x in ref_dict:
                    text = pi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                pir = Ref(parent=per,**ref_dict)
                pir.ref_type="primaryImage"
                pir.put()
            for ii in r.findall("image"):
                for x in ref_dict:
                    text = ii.find(x).text
                    ref_dict[x] = text if text is not None else ""
                iir = Ref(parent=per,**ref_dict)
                iir.ref_type="image"
                iir.put()
            for vi in r.findall("video"):
                for x in ref_dict:
                    text = vi.find(x).text
                    ref_dict[x] = text if text is not None else ""
                vir = Ref(parent=per,**ref_dict)
                vir.ref_type="video"
                vir.put()
            for si in r.findall("social"):
                for x in ref_dict:
                    text = si.find(x).text
                    ref_dict[x] = text if text is not None else ""
                sir = Ref(parent=per,**ref_dict)
                sir.ref_type="social"
                sir.put()
            for ei in r.findall("ext"):
                for x in ref_dict:
                    text = ei.find(x).text
                    ref_dict[x] = text if text is not None else ""
                eir = Ref(parent=per,**ref_dict)
                eir.ref_type="ext"
                eir.put()
        assert(Person.all().get() is not None) 
        self.redirect("/", permanent=True)

def main():
    application = webapp.WSGIApplication(
            [('/import', MainHandler),
            ('/upload', UploadHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
