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

"""
class Impact(db.Model):
    # human_ref = db.ReferenceProperty(Human)
    # economic_ref = db.ReferenceProperty(Economic)
"""


class Contact(db.Model):
    phone = db.StringProperty() 
    email = db.StringProperty()
    # mail_ref = db.ReferenceProperty(Mail)

class Info(db.Model):
    # All
    info_type = db.StringProperty()

    # Crisis, Organization only
    history = db.TextProperty()
    # loc_ref = db.ReferenceProperty(Location)

    # Crisis, Person only
    # time = db.ReferenceProperty(Time)

    # Crisis only
    info_help = db.StringProperty()
    resources = db.StringProperty()
    # impact = db.ReferenceProperty(Impact)

    # Organization only
    # contact_ref = db.ReferenceProperty(Contact)

    # Person only
    nationality = db.StringProperty()
    biography = db.TextProperty()

class Crisis(db.Model):
    crisis_id = db.StringProperty()
    name = db.StringProperty()
    # info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    orgs = db.ListProperty(str)
    persons = db.ListProperty(str)

class Organization(db.Model):
    org_id = db.StringProperty()
    name = db.StringProperty()
    # info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    crises = db.ListProperty(str)
    persons = db.ListProperty(str)

class Person(db.Model):
    person_id = db.StringProperty()
    name = db.StringProperty()
    # info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    crises = db.ListProperty(str)
    orgs = db.ListProperty(str)

class Ref(db.Model):
    ref_type = db.StringProperty()
    site = db.StringProperty()
    title = db.StringProperty()
    url = db.TextProperty()
    description = db.StringProperty()

class Ids(db.Model):
    model = db.StringProperty()
    ids = db.ListProperty(str)
