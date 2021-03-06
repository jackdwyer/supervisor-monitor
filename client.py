#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012
from urlparse import urlparse
import xmlrpclib
import socket
from xmlrpclib import ResponseError
import utils

class SupervisorClient(object):
    def __init__(self, uri, clientID, name=None, description=None, group=None):
        #uri is urlparse object
        self.URI = uri
        self.id = clientID
        self.name = name
        self.description = description
        self.group = group
        self.server = xmlrpclib.ServerProxy(self.URI.geturl())

    def get_details(self):
        details = self.get_process_info()
        try:
            totalProcesses = len(details)
            totalRunning = 0
            for service in details:
                if service['state'] == 20:
                    totalRunning += 1
        except TypeError:
            totalProcesses = 0
            totalRunning = 0
        
        
        return {"name": self.name, "ip":self.URI.netloc, "port":self.URI.port,
                "href":self.URI.geturl(), "details":details,
                "id":self.id, "totalClientProcesses":totalProcesses ,
                "totalClientRunning":totalRunning, "description":self.description}

    def get_process_info(self):
        try:
            return self.server.supervisor.getAllProcessInfo()
        except IOError:
            return None

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % (', '.join(map(repr, [self.name, self.URI.geturl()])))

if __name__ == '__main__':
    clientDetails = utils.parse_settings("../settings.conf")
    clients = []
    #Generate Supervisor clients
    for detail in clientDetails:
        if (len(detail) == 2):
            print detail
            continue
        if (len(detail) == 1):
            print detail
            continue
        else:
            print "Parsing Error in Settings, please check"
            sys.exit(1)