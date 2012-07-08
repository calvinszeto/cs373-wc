#!/usr/bin/env python
#

#
# goodbyeworld.py
# Handles the Export feature
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

class ExportHandler(webapp.RequestHandler):
    def get(self):
        """
        Handles the export feature of the GAE application.
        Called at calvins-cs373-wc.appspot.com/export
        """
        self.response.headers.add_header('content-type','text/xml')
        crises = Crisis.all()
        infos = Info.all()
        times = Time.all()
        locs = Location.all()
        humans = Human.all()
        economics = Economic.all()
        orgs = Organization.all()
        peeps = Person.all()
        template_values = {
            'crises':crises
            }
        path = os.path.join(os.path.dirname(__file__), 'template.xml')
        self.response.out.write(template.render(path, template_values))
        """
        template_values = {
            'crisis0name': crises[0].name,
            'info0help': infos[0].info_help,
            'info0resources': infos[0].resources,
            'info0type': infos[0].info_type,
            'time0day': times[0].day,
            'time0month': times[0].month,
            'time0year': times[0].year,
            'loc0region': locs[0].region,
            'human0deaths': humans[0].deaths,
            'human0displaced': humans[0].displaced,
            'human0injured': humans[0].injured,
            'human0missing': humans[0].missing,
            'economic0amount': economics[0].amount,
            'economic0currency': economics[0].currency,
            'crisis1name': crises[1].name,
            'time1day': times[1].day,
            'time1month': times[1].month,
            'time1year': times[1].year,
            'human1deaths': humans[1].deaths,
            'human1displaced': humans[1].displaced,
            'human1injured': humans[1].injured,
            'human1missing': humans[1].missing,
            'economic1amount': economics[1].amount,
            'crisis2name': crises[2].name,
            'time2day': times[2].day,
            'time2month': times[2].month,
            'time2year': times[2].year,
            'loc2country': locs[2].country,
            'human2deaths': humans[2].deaths,
            'human2displaced': humans[2].displaced,
            'human2injured': humans[2].injured,
            'human2missing': humans[2].missing,
            'economic2amount': economics[2].amount,
            'crisis3name': crises[3].name,
            'info3history': infos[3].history,
            'info3help': infos[3].info_help,
            'info3type': infos[3].info_type,
            'time3day': times[3].day,
            'time3month': times[3].month,
            'time3year': times[3].year,
            'loc3city': locs[3].city,
            'loc3country': locs[3].country,
            'human3deaths': humans[3].deaths,
            'human3displaced': humans[3].displaced,
            'human3injured': humans[3].injured,
            'human3missing': humans[3].missing,
            'economic3amount': economics[3].amount,
            'economic3currency': economics[3].currency,
            }
        """


def main():
    application = webapp.WSGIApplication(
            [('/export', ExportHandler),
            ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
