#!/usr/bin/env python
#

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import urllib
from Models import *

from xml.etree.ElementTree import ElementTree
from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

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

class MergeMainHandler(webapp.RequestHandler):
    def get(self):
        """
        Handles the import merge feature by posting the HTML which accepts a file.
        Then file is stored as a blob and UploadHandler is called.
        """
        upload_url = blobstore.create_upload_url('/upload')
        template_values = {
            'upload_url':upload_url,
            'type':'Merge'
        }
        path = os.path.join(os.path.dirname(__file__), '../templates/import.html')
        self.response.out.write(template.render(path, template_values))

class CrisisServeHandler(webapp.RequestHandler):
    def post(self):
        """
        Worker method that imports a single Crisis
        """
        resource = self.request.get('blob')
        crisis_id = self.request.get('crisis_id')
        blob_info = blobstore.BlobInfo.get(resource)
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        t1 = Ids.all().filter('model =', 'crisis').get()
        crisis_ids = Ids(model = "crisis", ids = []) if t1 is None else t1
        exists = crisis_id in crisis_ids.ids
        if not exists:
            # Add id to id list
            crisis_ids.ids.append(crisis_id)
            crisis_ids.put()
        for c in tree.findall("crisis"):
            cris_id = c.attrib["id"]
            if cris_id == crisis_id:
                if exists:
                    crisisObj = Crisis.all().filter('crisis_id =',crisis_id).get().delete() 
                for x in crisis_dict:
                    text = c.find(x).text
                    crisis_dict[x] = text if text is not None else ""
                cris = Crisis(**crisis_dict)
                cris.crisis_id = cris_id
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

class OrgServeHandler(webapp.RequestHandler):
    def post(self):
        """
        Worker for importing an Organization
        """
        resource = self.request.get('blob')
        organization_id = self.request.get('organization_id')
        blob_info = blobstore.BlobInfo.get(resource)
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        t2 = Ids.all().filter('model =', 'organization').get()
        organization_ids = Ids(model = "organization", ids = []) if t2 is None else t2
        exists = organization_id in organization_ids.ids
        for o in tree.findall("organization"):
            org_id = o.attrib["id"]
            if org_id == organization_id:
                if exists:
                    orgObj = Organization.all().filter('org_id =',organization_id).get().delete()
                else:
                    for x in org_dict:
                        text = o.find(x).text
                        org_dict[x] = text if text is not None else ""
                    org = Organization(**org_dict)
                    org.org_id = org_id
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
                    organization_ids.ids.append(organization_id)
                    organization_ids.put()

class PersonServeHandler(webapp.RequestHandler):
    def post(self):
        """
        Worker for importing a Person
        """
        resource = self.request.get('blob')
        person_id = self.request.get('person_id')
        blob_info = blobstore.BlobInfo.get(resource)
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        t3 = Ids.all().filter('model =', 'person').get()
        person_ids = Ids(model = "person", ids = []) if t3 is None else t3
        exists = person_id in person_ids.ids
        for p in tree.findall("person"):
            per_id = p.attrib["id"]
            if per_id == person_id:
                if exists:
                    personObj = Person.all().filter('person_id =',person_id).get().delete()
                else:
                    for x in person_dict:
                        text = p.find(x).text
                        person_dict[x] = text if text is not None else ""
                    per = Person(**person_dict)
                    per.person_id = person_id
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
                    person_ids.ids.append(person_id)
                    person_ids.put()

class MergeServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        """
        Handles the import merge of a file into the GAE Models.
        Searches for specific tags per the Schema and quits if file is invalid.
        """
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        tree = ElementTree()
        br = blob_info.open()
        tree.parse(br)
        # Crises
        for c in tree.findall("crisis"):
            cris_id = c.attrib["id"]
            taskqueue.add(url='/crisisserve', params={'blob': blob_info.key(), 'crisis_id': cris_id})
        # Organizations
        for o in tree.findall("organization"):
            org_id = o.attrib["id"]
            taskqueue.add(url='/orgserve', params={'blob': blob_info.key(), 'organization_id': org_id})
        # Person
        for p in tree.findall("person"):
            person_id = p.attrib["id"]
            taskqueue.add(url='/personserve', params={'blob': blob_info.key(), 'person_id': person_id})
        self.redirect("/", permanent=True)

def main():
    application = webapp.WSGIApplication(
            [('/importmerge', MergeMainHandler),
             ('/mergeserve/([^/]+)?', MergeServeHandler),
             ('/crisisserve', CrisisServeHandler),
             ('/orgserve', OrgServeHandler),
             ('/personserve', PersonServeHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
