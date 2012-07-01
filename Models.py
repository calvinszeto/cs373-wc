from google.appengine.ext import db

class Crisis(db.Model):
    name = db.StringProperty()
    # info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    # org_ref = db.ReferenceProperty(Organization)
    # person_ref = db.ReferenceProperty(Person)
