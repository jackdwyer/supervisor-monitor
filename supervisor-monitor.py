#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012

from urlparse import urlparse
from flask import Flask
from flask import render_template
import xmlrpclib
from lib import SupervisorClient, utils

app = Flask(__name__)
app.debug = True

@app.route('/')
def list_all():
    supervisors = []
    for supervisor in app.clients:
        supervisors.append(supervisor.get_details())
    return render_template('list.html', supervisors=supervisors)



if __name__ == "__main__":
    clientDetails = utils.parse_settings("settings.conf")
    clients = []
    #Generate Supervisor clients
    for detail in clientDetails:
        uri = urlparse(detail[0])
        try:
            name = detail[1]
        except IndexError:
            name = None
        
        clients.append(SupervisorClient(uri, name))
        


    app.clients = clients
    app.run(host='0.0.0.0')
