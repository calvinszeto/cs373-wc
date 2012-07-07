from google.appengine.ext import db

#
# Models.py
# Holds the GAE Models for world crisis app.
#

class Mail(db.Model):
    address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    mail_zip = db.StringProperty()

class Time(db.Model):
    time = db.StringProperty()
    day = db.StringProperty()
    month = db.StringProperty()
    year = db.StringProperty()
    misc = db.StringProperty()

class Location(db.Model):
    city = db.StringProperty()
    region = db.StringProperty()
    country = db.StringProperty()

class Human(db.Model):
    deaths = db.StringProperty()
    displaced = db.StringProperty()
    injured = db.StringProperty()
    missing = db.StringProperty()
    misc = db.StringProperty()

class Economic(db.Model):
    amount = db.StringProperty()
    currency = db.StringProperty()
    misc = db.StringProperty()

class Impact(db.Model):
    human_ref = db.ReferenceProperty(Human)
    economic_ref = db.ReferenceProperty(Economic)


class Contact(db.Model):
    phone = db.StringProperty() 
    email = db.StringProperty()
    mail_ref = db.ReferenceProperty(Mail)

class Info(db.Model):
    # All
    info_type = db.StringProperty()

    # Crisis, Organization only
    history = db.TextProperty()
    loc_ref = db.ReferenceProperty(Location)

    # Crisis, Person only
    time = db.ReferenceProperty(Time)

    # Crisis only
    info_help = db.StringProperty()
    resources = db.StringProperty()
    impact = db.ReferenceProperty(Impact)

    # Organization only
    contact_ref = db.ReferenceProperty(Contact)

    # Person only
    nationality = db.StringProperty()
    biography = db.StringProperty()

class Crisis(db.Model):
    name = db.StringProperty()
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()

class Organization(db.Model):
    name = db.StringProperty()
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()

class Person(db.Model):
    name = db.StringProperty()
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()

class WCObject(db.Model):
    crisis_ref = db.ReferenceProperty(Crisis)
    person_ref = db.ReferenceProperty(Person)
    org_ref = db.ReferenceProperty(Organization)

class Ref(db.Model):
    crisis = db.ReferenceProperty(Crisis, collection_name='refs')
    org= db.ReferenceProperty(Organization, collection_name='refs')
    person = db.ReferenceProperty(Person, collection_name='refs')
    site = db.StringProperty()
    title = db.StringProperty()
    url = db.StringProperty()
    description = db.StringProperty()

