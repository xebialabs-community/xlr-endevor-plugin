#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sets
import sys
from urllib import urlencode
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

HTTP_SUCCESS = sets.Set([200, 201, 202, 203, 204, 205, 206, 207, 208])
HTTP_ERROR = sets.Set([400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,412, 413, 414, 415])

class Endevor_Client(object):
    def __init__(self, httpConnection, username=None, password=None):
        self.httpConnection = httpConnection
        self.logger = LoggerFactory.getLogger("Endevor")
        self.httpRequest = HttpRequest(httpConnection, username, password)

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return Endevor_Client(httpConnection, username, password)

    def testServer(self):
        endevorUrl = 'EndevorService/rest/application.wadl'
        self.logger.error("Open URL %s" % endevorUrl)
        response = self.httpRequest.get(endevorUrl, contentType='application/*')
        if response.getStatus() in HTTP_SUCCESS:
            data = response.getResponse()
            self.logger.error("=====================\n%s\n=====================\n" % data )
            return
        self.logger.error("HTTP ERROR Code = %s" % response.getStatus() )
        self.throw_error(response)

    def list_all_configurations(self):
        endevorUrl = 'EndevorService/rest'
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info("List All Configurations Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", ['config1','config2','config3'])
        self.throw_error(response)

    def list_configuration_parameters(self, instance):
        endevorUrl = 'EndevorService/rest/%s' % instance
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "List Configuration Parameters Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
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

        self.logger.info("List Packages %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.get(endevorUrl.replace('&','?',1), contentType='application/json')
        data = json.loads(response.getResponse())
        if response.getStatus() in HTTP_SUCCESS:
            pkgList=[]
            for pkg in data['data']:
                self.logger.info( "PKG = %s" % pkg )
                if( "pkgId" in pkg ):
                    pkgList.append( pkg['pkgId'] )
                if( "PKG ID" in pkg ):
                    pkgList.append( pkg['PKG ID'] )
            return (data['returnCode'], data['reasonCode'], pkgList)
        else:
            self.logger.error("Return Code = %s" % data['returnCode'])
            self.logger.error("Reason Code = %s" % data['reasonCode'])
            self.logger.error("Message     = %s" % data['messages'])
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

        self.logger.error("Update Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Update Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor package info")
        self.throw_error(response)

    def create_package(self, instance, package, ewfromdate, ewfromtime, ewtodate, ewtotime, packageType, shareable, backout, append, promotion, fromPackage, fromDSN, fromMember, doNotValidate):
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

        self.logger.error("Create Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.post(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Update Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
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

        self.logger.error("Cast Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Cast Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor cast result")
        self.throw_error(response)

    def approve_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Approve' % (instance, package)

        self.logger.error("Approve Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Approve Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
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

        self.logger.error("Execute Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.error( "Execute Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor execute result")
        self.throw_error(response)

    def backout_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backout' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement)
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element)

        self.logger.error("Backout Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Backout Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor backout result")
        self.throw_error(response)

    def backin_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backin' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement)
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element)

        self.logger.error("Backin Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Backin Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
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

        self.logger.error("Commit Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Commit Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
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

        self.logger.error("Ship Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Ship Package Return \n%s\n" % data )
            return (data['returnCode'], data['reasonCode'], data['messages'])
        self.logger.error("Return Code = %s" % data['returnCode'])
        self.logger.error("Reason Code = %s" % data['reasonCode'])
        self.logger.error("Message     = %s" % data['messages'])
        self.throw_error(response)

    def delete_package(self, instance, package, olderThan, status):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (instance, package)

        if olderThan:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, olderThan)
        if status:
            endevorUrl = "%s&status=%s" % (endevorUrl, status)

        self.logger.error("Delete Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.delete(endevorUrl.replace('&','?',1), contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Delete Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor delete result")
        self.throw_error(response)

    def reset_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Reset' % (instance, package)

        self.logger.error("Reset Package %s " % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        if response.getStatus() in HTTP_SUCCESS:
            data = json.loads(response.getResponse())
            self.logger.info( "Reset Package Return \n%s\n" % data )
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", "Endevor reset result")
        self.throw_error(response)

    def throw_error(self, response):
        self.logger.error("Error from EndevorService, HTTP Return: %s\n" % ( response.getStatus() ) )
        sys.exit(response.getStatus())
