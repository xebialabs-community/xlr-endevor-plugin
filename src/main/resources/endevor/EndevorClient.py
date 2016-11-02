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

HTTP_SUCCESS = sets.Set([200])

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
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", ['config1','config2','config3'])
        self.throw_error(response)

    def list_configuration_parameters(self, instance):
        endevorUrl = 'EndevorService/rest/%s' % instance
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", {'param1':'value1','param2':'value2','param3':'value3'})
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
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", ['package1','package2','package3'])
        self.throw_error(response)

    def update_package(self, instance, package, ewfromdate, ewfromtime, ewtodate, ewtotime, packageType, shareable, backout, append, promotion, fromPackage, fromDSN, fromMember, doNotValidate):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (instance, package)
        
        if ewfromdate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewfromdate) 
        if ewfromtime:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, ewfromtime) 
        if ewtodate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewtodate) 
        if ewtotime:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, ewtotime) 
        if packageType:
            endevorUrl = "%s&type=%s" % (endevorUrl, packageType) 
        if shareable:
            endevorUrl = "%s&shareable=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&shareable=%s" % (endevorUrl, "no")
        if backout:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "no")
        if append:
            endevorUrl = "%s&append=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&append=%s" % (endevorUrl, "no")
        if promotion:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, "yes") 
        else:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, "no")
        if fromPackage:
            endevorUrl = "%s&fromPackage=%s" % (endevorUrl, fromPackage) 
        if fromDSN:
            endevorUrl = "%s&fromDSN=%s" % (endevorUrl, fromDSN) 
        if fromMember:
            endevorUrl = "%s&fromMember=%s" % (endevorUrl, fromMember)
        if doNotValidate:
            endevorUrl = "%s&do-not-validate=%s" % (endevorUrl, "true") 
        
        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor package info")
        self.throw_error(response)

    def cast_package(self, instance, package, ewfromdate, ewfromtime, ewtodate, ewtotime, validateComponents, backout):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Cast' % (instance, package)

        if ewfromdate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewfromdate) 
        if ewfromtime:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, ewfromtime) 
        if ewtodate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewtodate) 
        if ewtotime:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, ewtotime) 
        if validateComponents:
            endevorUrl = "%s&validate-components=%s" % (endevorUrl, validateComponents)
        if backout:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "no")

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor cast result")
        self.throw_error(response)

    def approve_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Approve' % (instance, package)

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor approve result")
        self.throw_error(response)

    def execute_package(self, instance, package, ewfromdate, ewfromtime, ewtodate, ewtotime, status):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Execute' % (instance, package)

        if ewfromdate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewfromdate) 
        if ewfromtime:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, ewfromtime) 
        if ewtodate:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, ewtodate) 
        if ewtotime:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, ewtotime) 
        if status:
            endevorUrl = "%s&status=%s" % (endevorUrl, status) 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor execute result")
        self.throw_error(response)

    def backout_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backout' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement) 
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element) 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor backout result")
        self.throw_error(response)

    def backin_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backin' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement) 
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element) 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor backin result")
        self.throw_error(response)

    def commit_package(self, instance, package, olderThan, deletePromotionHistory):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Commit' % (instance, package)

        if olderThan:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, olderThan) 
        if deletePromotionHistory:
            endevorUrl = "%sdelete-promotion-history=%s" % (endevorUrl, "true") 
        else:
            endevorUrl = "%sdelete-promotion-history=%s" % (endevorUrl, "false") 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor commit result")
        self.throw_error(response)

    def ship_package(self, instance, package, destination, option, prefix):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Ship' % (instance, package)

        if destination:
            endevorUrl = "%s&destination=%s" % (endevorUrl, destination) 
        if option:
            endevorUrl = "%s&option=%s" % (endevorUrl, option) 
        if prefix:
            endevorUrl = "%s&prefix=%s" % (endevorUrl, prefix) 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor ship result")
        self.throw_error(response)

    def delete_package(self, instance, package, olderThan, status):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (instance, package)

        if olderThan:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, olderThan) 
        if status:
            endevorUrl = "%s&status=%s" % (endevorUrl, status) 

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.delete(endevorUrl.replace('&','?',1), contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor delete result")
        self.throw_error(response)

    def reset_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Reset' % (instance, package)

        print endevorUrl.replace('&','?',1)
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
# TO-DO:  determine structure of returned data
#           data = json.loads(response.getResponse())
#           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor reset result")
        self.throw_error(response)

    def throw_error(self, response):
        print "Error from EndevorService, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)
