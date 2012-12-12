#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012

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
        if (len(detail) == 2):
            clients.append(SupervisorClient.SupervisorClient(detail[0], name=detail[1]))
            continue
        if (len(detail) == 1):
            clients.append(SupervisorClient.SupervisorClient(detail[0],))
            continue
        else:
            print "Parsing Error in Settings, please check"
            sys.exit(1)

    app.clients = clients

    app.run(host='0.0.0.0')
