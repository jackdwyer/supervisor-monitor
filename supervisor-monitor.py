#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012

import argparse, sys

from urlparse import urlparse
from flask import Flask
from flask import render_template
import xmlrpclib
from lib import SupervisorClient, utils

app = Flask(__name__)

@app.route('/')
def list_all():
    supervisors = []
    for supervisor in app.clients:
        supervisors.append(supervisor.get_details())
    return render_template('list.html', supervisors=supervisors)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store', dest='port', default=5000,
                        help='Set port to run on')

    parser.add_argument('--debug', action='store_true', default=False,
                    dest='debug',
                    help='Use to start server in debug mode')

    results = parser.parse_args()

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
        
    try:
        results.port = int(results.port)
    except ValueError:
        print "Error: must use a valid number for port"
        sys.exit(1)


    app.clients = clients
    app.run(host='0.0.0.0', debug=results.debug, port=results.port)
