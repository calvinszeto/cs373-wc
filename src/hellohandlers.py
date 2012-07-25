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

class CrisisHandler(webapp.RequestHandler):
    def post(self):
        def txn():
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
        db.run_in_transaction(txn)

def main():
    application = webapp.WSGIApplication(
            [('/crisismerge', CrisisHandler)
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
