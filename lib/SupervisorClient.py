#!/usr/bin/env python2.7
#Jack Dwyer 12-12-2012
from urlparse import urlparse
import xmlrpclib
from xmlrpclib import ResponseError
import utils 

class SupervisorClient(object):
    def __init__(self, url, name=None):
        self._url = urlparse(url, scheme='http')
        self._name = name    
        self._server = xmlrpclib.ServerProxy(self.get_url())

    def get_details(self):
        return {"name":self._name, "ip":self.get_url(), "port":self.get_port(), "href":self.get_url(), "details":self.get_process_info()}

    def get_process_info(self):
        try:
            return self._server.supervisor.getAllProcessInfo()
        except ResponseError:
            return []

    def get_port(self):
        return self._url.port

    def get_url(self):
        return self._url.geturl()

    def get_name(self):
        return self._name

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % (', '.join(map(repr, [self._name, self._url])))

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