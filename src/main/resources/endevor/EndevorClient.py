#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sets
import sys
from urllib import urlencode
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

HTTP_SUCCESS = sets.Set([200,404])

class Endevor_Client(object):
    def __init__(self, httpConnection, username=None, password=None):
        self.httpConnection = httpConnection
        self.httpRequest = HttpRequest(httpConnection, username, password)

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return Endevor_Client(httpConnection, username, password)

    def list_all_configurations(self):
        endevorUrl = 'EndevorService/rest'
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS: 
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return data['key']
            return ['config1','config2','config3']
        self.throw_error(response)

    def list_configuration_parameters(self, instance):
        endevorUrl = 'EndevorService/rest/%s' % instance
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return data['key']
            return {'param1':'value1','param2':'value2','param3':'value3'}
        self.throw_error(response)

    def list_packages(self, instance, status, packageType, enterprise, promotion):
        endevorUrl = 'EndevorService/rest/%s/packages' % instance
        
        if status:
            for item in status:
                endevorUrl = "%s&status=%s" % (endevorUrl, item) 
        if packageType:
            endevorUrl = "%s&type=%s" % (endevorUrl, packageType) 
        if enterprise:
            endevorUrl = "%s&enterprise=%s" % (endevorUrl, enterprise) 
        if promotion:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, promotion) 
        
        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.get(endevorUrl.replace('&','?',1), contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return data['key']
            return ['package1','package2','package3']
        self.throw_error(response)

# TO-DO:
#   def update_packages(self):
#   def cast_package(self):
#   def approve_packages(self):
#   def execute_package(self):
#   def backout_package(self):
#   def backin_package(self):
#   def commit_package(self):
#   def ship_package(self):
#   def delete_package(self):
#   def reset_package(self):

    def throw_error(self, response):
        print "Error from EndevorService, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)
