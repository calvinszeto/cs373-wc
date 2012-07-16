import unittest
from helloworld import *
from goodbyeworld import *
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree

class TestWC1(unittest.TestCase):

    def test_Crisis_1 (self):
        """
        Test the Crisis Model
        """
        cris = Crisis()
        cris.name = "Deepwater Horizon Oil Spill"
        self.assertTrue(cris.name == "Deepwater Horizon Oil Spill")

    def test_Crisis_2 (self):
        """
        Test the Crisis Model
        """
        cris = Crisis()
        cris.misc = ""
        self.assertTrue(cris.misc == "")

    def test_Crisis_3 (self):
        """
        Test the Crisis Model
        """
        cris = Crisis()
        cris.orgs = ["bp"]
        self.assertTrue(cris.orgs[0] == "bp")

    def test_Organization_1 (self):
        """
        Test the Organization Model
        """
        org = Organization()
        self.assertTrue(org.name != "")

    def test_Organization_2 (self):
        """
        Test the Organization Model
        """
        org = Organization()
        self.assertTrue(org.name is None) 

    def test_Organization_3 (self):
        """
        Test the Organization Model
        """
        org = Organization()
        org.org_id = "bp"
        self.assertTrue(org.org_id == "bp") 

    def test_Person_1 (self):
        """
        Test the Person Model
        """
        peps = Person()
        peps.name = "Connor Bowman"
        self.assertTrue(peps.name is "Connor Bowman")

    def test_Person_2 (self):
        """
        Test the Person Model
        """
        peps = Person()
        peps.misc = "Connor Bowman"
        self.assertTrue(peps.misc == "Connor Bowman")

    def test_Person_3 (self):
        """
        Test the Person Model
        """
        peps = Person()
        peps.crises = ["Connor Bowman"]
        self.assertTrue(peps.crises == ["Connor Bowman"])

    def test_Time_1 (self):
        """
        Test the Time Model
        """
        t = Time()
        t.month = "4" 
        self.assertTrue(t.month == "4")

    def test_Time_2 (self):
        """
        Test the Time Model
        """
        t = Time()
        t.day = "30"
        self.assertTrue(t.day == "30")

    def test_Time_3 (self):
        """
        Test the Time Model
        """
        t = Time()
        t.year = "1970"
        self.assertTrue(t.year == "1970")

    def test_Time_4 (self):
        """
        Test the Time Model
        """
        t = Time()
        t.time = "11:30"
        self.assertTrue(t.time == "11:30")

    def test_Mail_1 (self):
        """
        Test the Mail Model
        """
        m = Mail()
        m.address = "1 Main St."
        self.assertTrue(m.address == "1 Main St.")

    def test_Mail_2 (self):
        """
        Test the Mail Model
        """
        m = Mail()
        m.city = "Austin"
        self.assertTrue(m.city == "Austin")

    def test_Mail_3 (self):
        """
        Test the Mail Model
        """
        m = Mail()	
        m.state = "TX"
        self.assertTrue(m.state == "TX")

    def test_Mail_4 (self):
        """
        Test the Mail Model
        """
        m = Mail()
        m.country = "USA"
        self.assertTrue(m.country == "USA")

    def test_Mail_5 (self):
        """
        Test the Mail Model
        """
        m = Mail()
        m.mail_zip = "78705"
        self.assertTrue(m.mail_zip == "78705")

    def test_Location_1 (self):
        """
        Test the Location Model
        """
        l = Location()
        l.city = "Austin"
        self.assertTrue(l.city == "Austin")

    def test_Location_2 (self):
        """
        Test the Location Model
        """
        l = Location()
        l.region = "Austin"
        self.assertTrue(l.region == "Austin")

    def test_Location_3 (self):
        """
        Test the Location Model
        """
        l = Location()
        l.country = "Austin"
        self.assertTrue(l.country == "Austin")

    def test_XML_Parser_1 (self):
        """
        Test that ElementTree can find the crisis/name tag
        """
        d = p.find("crisis/name")
        self.assertTrue(d.text == "Deepwater Horizon Oil Spill")

    def test_XML_Parser_2 (self):
        """
        Test that ElementTree can find the crisis/info/loc/region tag
        """
        d = p.find("crisis/info/loc/region")
        self.assertTrue(d.text == "Gulf of Mexico")

    def test_XML_Parser_3 (self):
        """
        Test that ElementTree can find the crisis/info/impact/human/deaths tag
        """
        d = p.find("crisis/info/impact/human/deaths")
        self.assertTrue(d.text == "11")

    def test_Model_Constructor_1 (self):
        """
        Test constructing an Info by unpacking a dict
        """
        info_dict = {"history":"1960","resources":"gold"}
        info = Info(**info_dict)
        self.assertTrue(info.history == "1960")
        self.assertTrue(info.resources == "gold")
        
    def test_Model_Constructor_2 (self):
        """
        Test constructing a Human by unpacking a dict
        """
        human_dict = {"deaths":"1","displaced":"2","injured":"3","missing":"4","misc":"5"}
        human = Human(**human_dict)
        self.assertTrue(human.deaths == "1")
        self.assertTrue(human.displaced == "2")
        self.assertTrue(human.injured == "3")
        self.assertTrue(human.missing == "4")
        self.assertTrue(human.misc == "5")

    def test_Model_Constructor_3 (self):
        """
        Test constructing a Contact by unpacking a dict
        """
        org_contact_dict = {"phone":"1","email":"1@spiderman.com"}
        contact = Contact(**org_contact_dict)
        self.assertTrue(contact.phone == "1")
        self.assertTrue(contact.email == "1@spiderman.com")

    def test_Datastore_1 (self):
        """
        Testing putting and pulling a Crisis from the datastore
        """
        # Crises
        for c in p.findall("crisis"):
            for x in crisis_dict:
                text = c.find(x).text
                crisis_dict[x] = text if text is not None else ""
            cris = Crisis(**crisis_dict)
            cris.put()
        crises = Crisis.all()
        self.assertTrue(crises[0].name == "Deepwater Horizon Oil Spill")

    def test_Datastore_2 (self):
        """
        Testing that parser does not find an organization and thus datastore is empty
        """
        # Crises
        for c in p.findall("organization"):
            for x in org_dict:
                text = c.find(x).text
                org_dict[x] = text if text is not None else ""
            cris = Crisis(**crisis_dict)
            cris.put()
        crises = Crisis.all()
        self.assertTrue(crises.get() is None)

    def test_Datastore_3 (self):
        """
        Testing pulling the Crisis - Orgs attribute from the datastore
        """
        # Crises
        for c in p.findall("crisis"):
            for x in crisis_dict:
                text = c.find(x).text
                crisis_dict[x] = text if text is not None else ""
            cris = Crisis(**crisis_dict)
            # Crisis - Org
            for org in c.findall("org"):
                cris.orgs.append(org.attrib["idref"]) 
            cris.put()
        crises = Crisis.all()
        self.assertTrue(crises[0].orgs[0]== "bp")

    def test_Parent_Child_1 (self):
        """
        Testing a Crisis-Info parent-child relationship
        """
        cris = Crisis()
        cris.name = "Spiderman"
        cris.put()
        info = Info(parent=cris)
        info.info_type = "Arachnid"
        info.put()
        crises = Crisis.all()
        infos = Info.all().ancestor(crises.get()).get()
        self.assertTrue(infos.info_type == "Arachnid")

    def test_Parent_Child_2 (self):
        """
        Testing a Info-Location parent-child relationship
        """
        info = Info()
        info.info_type = "Arachnid"
        info.put()
        loc = Location(parent=info)
        loc.city = "New York City"
        loc.put()
        infos = Info.all()
        locs = Location.all().ancestor(infos.get()).get()
        self.assertTrue(locs.city == "New York City")

    def test_Parent_Child_3 (self):
        """
        Testing a Crisis-Ref parent-child relationship
        """
        cris = Crisis()
        cris.name = "Spiderman"
        cris.put()
        ref = Ref(parent=cris)
        ref.url = "www.spiderman.com"
        ref.put()
        crises = Crisis.all()
        refs = Ref.all().ancestor(crises.get()).get()
        self.assertTrue(refs.url == "www.spiderman.com")

p = xml.etree.ElementTree.fromstring("""<worldcrisis>
<crisis id = "deepwater">
<name>Deepwater Horizon Oil Spill</name>
<info>
<history></history>
<help> Volunteering along the gulf to help clean</help>
<resources> Help cleaning spill and wildlife</resources>
<type>Wellhead Blowout and Oil Spill</type>
<time>
<time></time>
<day>20</day>
<month>4</month>
<year>2010</year>
<misc></misc>
</time>
<loc>
<city></city>
<region>Gulf of Mexico</region>
<country></country>
</loc>
<impact>
<human>
<deaths>11</deaths>
<displaced>0</displaced>
<injured>0</injured>
<missing>0</missing>
<misc></misc>
</human>
<economic>
<amount>30000000000</amount>
<currency>dollars</currency>
<misc></misc>
</economic>
</impact>
</info>
<ref>
            <primaryImage>
                <site></site>
<title></title>
<url></url>
<description></description>
            </primaryImage>
<image>
                <site></site>
<title>Deepwater Horizon</title>
<url>http://www.thebuzzmedia.com/wp-content/uploads/2010/06/bp-oil-spill-bird-covered-in-oil.jpg</url>
<description></description>
</image>
<video>
<site>Youtube</site>
<title></title>
<url>http://www.youtube.com/watch?v=lY-PikuXTYY</url>
<description></description>
</video>
<social>
                <site></site>
<title>Facebook</title>
<url>http://www.facebook.com/BPOilCrisisInTheGulf?ref=ts</url>
                <description></description>
</social>
<ext>
                <site></site>
<title>Wikipedia</title>
<url>http://en.wikipedia.org/wiki/Deepwater_Horizon_oil_spill#Consequences</url>
<description></description>
</ext>
</ref>
<misc></misc>
<org idref = "bp"/>
<person idref = "feinberg"/>
</crisis>
</worldcrisis>""")
	
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestWC1.testName']
    unittest.main()
