#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012

import argparse, sys

from urlparse import urlparse
from flask import Flask, abort, redirect, url_for
from flask import render_template
import xmlrpclib
import utils
from client import SupervisorClient

app = Flask(__name__)


@app.route('/group/<selectedGroup>')
def group_list(selectedGroup):
    fullDetails = {}
    supervisors = {}
    fullDetails["totalRunning"] = 0
    fullDetails["totalProcesses"] = 0

    tables = 0
    for group, value in app.clients.items():
        if group == selectedGroup:
            supervisors[group] = []
            
            for supervisor in value:
                details = supervisor.get_details()
                supervisors[group].append(details)
                fullDetails["totalRunning"] += details["totalClientRunning"]
                fullDetails["totalProcesses"] += details["totalClientProcesses"]
                
                tables += 1
    
    if tables == 0:
        return redirect(url_for('list_all'))
        
    
    
    fullDetails["totalTables"] = tables
    fullDetails["supervisors"] = supervisors
    fullDetails["groups"] = app.groups
    return render_template('list.html', details=fullDetails)  


@app.route('/')
def list_all():
    fullDetails = {}
    fullDetails["totalRunning"] = 0
    fullDetails["totalProcesses"] = 0
    print app.clients
    
    supervisors = {}
    for group, value in app.clients.items():
        supervisors[group] = []
        for supervisor in value:
            details = supervisor.get_details()
            supervisors[group].append(details)
            fullDetails["totalRunning"] += details["totalClientRunning"]
            fullDetails["totalProcesses"] += details["totalClientProcesses"]
        
    fullDetails["totalTables"] = app.totalTables
    fullDetails["supervisors"] = supervisors
    fullDetails["groups"] = app.groups
    return render_template('list.html', details=fullDetails)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', action='store', default=5000,
                        help='Set port to run on')

    parser.add_argument('--debug', action='store_true', default=False,
                    help='Use to start server in debug mode')

    results = parser.parse_args()

    groups = []
    clients = {}
    #Generate Supervisor clients
    clientID = 0
    #for detail in clientDetails:
    #    uri = urlparse(detail[0])
    #    try:
    #        name = detail[1]
    #    except IndexError:
    #        name = None
    #    
    #    clients.append(SupervisorClient(uri, clientID, name))
        
    
    supervisors = utils.read_yaml()
    for key, value in supervisors.items():
        uri = urlparse("%s%s%s%s%s" % (value["scheme"], "://", str(key), ":", str(value["port"])))
        client = SupervisorClient(uri, clientID)
        
        #Add extra details if avaliable
        try:
            client.name = value["name"]
        except KeyError:
            pass
        try:
            client.group = value["group"]
            if not value["group"] in groups:
                groups.append(value["group"])
                
        except KeyError:
            value["group"] = "default"
            groups.append(value["group"])

            
        try:
            client.description = value["description"]
        except KeyError:
            pass


        try:
            clients[value["group"]].append(client)
        except KeyError:
            clients[value["group"]] = []
            clients[value["group"]].append(client)

        #clients.append(client)
        clientID += 1


    print clients

    app.clients = clients
    app.groups = sorted(groups, key=str.lower)
    app.totalTables = clientID
    app.run(host='0.0.0.0', debug=results.debug, port=results.port)
