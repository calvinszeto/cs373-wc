from google.appengine.ext import db
from Models import *

class WCObject(db.Model):
    crisis_ref = db.ReferenceProperty(Crisis)
    person_ref = db.ReferenceProperty(Person)
    org_ref = db.ReferenceProperty(Organization)
