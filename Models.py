from google.appengine.ext import db

class Crisis(db.Model):
    name = db.StringProperty()
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    org_ref = db.ReferenceProperty(Organization)
    person_ref = db.ReferenceProperty(Person)

class Organization(db.Model):
    name = db.StringProperty()
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    crisis_ref = db.ReferenceProperty(Crisis)
    person_ref = db.ReferenceProperty(Person)

class Person(db.Model):
    name_ref = db.ReferenceProperty(Name)
    info_ref = db.ReferenceProperty(Info)
    misc = db.StringProperty()
    crisis_ref = db.ReferenceProperty(Crisis)
    org_ref = db.ReferenceProperty(Organization)

class Info(db.Model):
    # All
    info_type = db.StringProperty()

    # Crisis, Organization only
    history = db.StringProperty()
    loc_ref = db.ReferenceProperty(Location)

    # Crisis only
    info_help = db.StringProperty()
    resources = db.StringProperty()
    time = db.ReferenceProperty(Time)
    impact = db.ReferenceProperty(Impact)

    # Organization only
    contact_ref = db.ReferenceProperty(Contact)

    # Person only
    birthdate = db.ReferenceProperty(Time)
    nationality = db.StringProperty()
    biography = db.StringProperty()

class Contact(db.Model):
    phone = db.StringProperty() 
    email = db.StringProperty()
    mail_ref = db.ReferenceProperty(Mail)

class Mail(db.Model):
    address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    mail_zip = db.StringProperty()

class Ref(db.Model):
    site = db.StringProperty()
    title = db.StringProperty()
    url = db.StringProperty()
    description = db.StringProperty()

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

class Impact(db.Model):
    human_ref = db.ReferenceProperty(Human)
    economic_ref = db.ReferenceProperty(Economic)

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
