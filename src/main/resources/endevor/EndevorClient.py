#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import traceback
import sets
import sys
import urllib
import json
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
        self.logger.error("List All Configurations Request %s" % endevorUrl)
        data = self.getJson(response)
        self.logger.error("List All Configurations Response=============\n%s\n==================" % data)
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['data'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def list_configuration_parameters(self, instance):
        endevorUrl = 'EndevorService/rest/%s' % instance
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        self.logger.error("List Configuration Parameters Request %s" % endevorUrl)
        data = json.loads(response.getResponse())
        self.logger.error("List Configuration Parameters Response=============\n%s\n==================" % data)
        if response.getStatus() in HTTP_SUCCESS:
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            return ("0000", "0000", {'param1':'value1','param2':'value2','param3':'value3'})
        else:
            self.logBadReturnCodes(data)
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

        self.logger.error("List Packages Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.get(endevorUrl.replace('&','?',1), contentType='application/json')
        data = json.loads(response.getResponse())
        self.logger.error("List Packages Response=============\n%s\n==================" % data)
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
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def update_package(self, instance, package, description, ewfromdate, ewfromtime, ewtodate, ewtotime, packageType, shareable, backout, append, promotion, fromPackage, fromDSN, fromMember, doNotValidate):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (instance, package)

        if description:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, description)
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

        self.logger.error("Update Package Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = json.loads(response.getResponse())
        self.logger.error("Update Package Response=============\n%s\n==================" % data)
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['data'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_createpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (variables['instance'], variables['package'])

        if variables['description']:
            endevorUrl = "%s&description=%s" % (endevorUrl, urllib.quote(variables['description']))
        if variables['ewfromdate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewfromdate']))
        if variables['ewfromtime']:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, urllib.quote(variables['ewfromtime']))
        if variables['ewtodate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewtodate']))
        if variables['ewtotime']:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, urllib.quote(variables['ewtotime']))
        if variables['packageType']:
            endevorUrl = "%s&type=%s" % (endevorUrl, urllib.quote(variables['packageType']))
        if variables['shareable']:
            endevorUrl = "%s&shareable=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&shareable=%s" % (endevorUrl, "no")
        if variables['backout']:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "no")
        if variables['append']:
            endevorUrl = "%s&append=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&append=%s" % (endevorUrl, "no")
        if variables['promotion']:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, "no")
        if variables['fromPackage']:
            endevorUrl = "%s&fromPackage=%s" % (endevorUrl, urllib.quote(variables['fromPackage']))
        if variables['fromDSN']:
            endevorUrl = "%s&fromDSN=%s" % (endevorUrl, urllib.quote(variables['fromDSN']))
        if variables['fromMember']:
            endevorUrl = "%s&fromMember=%s" % (endevorUrl, urllib.quote(variables['fromMember']))
        if variables['doNotValidate']:
            endevorUrl = "%s&do-not-validate=%s" % (endevorUrl, "true")

        self.logger.error("Create Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.post(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        #self.logger.error("Create Package Return =============\n%s\n=============\n" % json.dumps(data, indent=4, sort_keys=True) )
        self.logger.error("HTTP Error Code %s" % response.getStatus())
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Create Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
            #return (data['returnCode'], data['reasonCode'], data['messages'])
        else:
            self.logBadReturnCodes(data)
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
        data = self.getJson(response)
        self.logger.error("Cast Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def approve_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Approve' % (instance, package)

        self.logger.error("Approve Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Approve Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
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
        data = self.getJson(response)
        self.logger.error("Execute Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def backout_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backout' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement)
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element)

        self.logger.error("Backout Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Backout Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def backin_package(self, instance, package, statement, element):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backin' % (instance, package)

        if statement:
            endevorUrl = "%s&statement=%s" % (endevorUrl, statement)
        if element:
            endevorUrl = "%s&element=%s" % (endevorUrl, element)

        self.logger.error("Backin Package Request %s" % endevorUrl.replace('&','?',1))
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Backin Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
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
        data = self.getJson(response)
        self.logger.error("Commit Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def ship_package(self, instance, package, destination, option, prefix):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Ship' % (instance, package)

        if destination:
            endevorUrl = "%s&destination=%s" % (endevorUrl, destination)
        if option:
            endevorUrl = "%s&option=%s" % (endevorUrl, option)
        if prefix:
            endevorUrl = "%s&prefix=%s" % (endevorUrl, prefix)

        self.logger.error("Ship Package Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Ship Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def delete_package(self, instance, package, olderThan, status):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (instance, package)

        if olderThan:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, olderThan)
        if status:
            endevorUrl = "%s&status=%s" % (endevorUrl, status)

        self.logger.error("Delete Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.delete(endevorUrl.replace('&','?',1), contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Delete Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def reset_package(self, instance, package):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Reset' % (instance, package)

        self.logger.error("Reset Package Request %s " % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Reset Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            return (data['returnCode'], data['reasonCode'], data['messages'], data['reports'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def getJson(self, response):
        self.setLastError("")
        data = {}
        try:
            data = json.loads(response.getResponse())
        except:
            tb = traceback.format_exc()
            self.logger.error("getJson EXCEPTION \n================\n%s\n=================" % tb)
            self.setLastError(tb)
            self.logger.error("getJson RAW RESPONSE \n================\n%s\n=================" % response.getResponse())
        return data

    def logBadReturnCodes(self, data):
        if ('returnCode' in data) & ('reasonCode' in data) & ('messages' in data):
            self.logger.error("Return Code = %s" % data['returnCode'])
            self.logger.error("Reason Code = %s" % data['reasonCode'])
            self.logger.error("Message     = %s" % data['messages'])
        else:
            tb = self.getLastError()
            self.logger.error("Return Codes EXCEPTION \n================\n%s\n=================" % tb)
            self.logger.error("REAL BAD RETURN OBJECT!!!!")
            self.setLastError("%s\nREAL BAD RETURN OBJECT!!!!" % tb)
            raise Exception(500)

    def setLastError(self, error):
        self.error = error

    def getLastError(self):
        return self.error

    def throw_error(self, response):
        self.logger.error("Error from EndevorService, HTTP Return: %s\n" % ( response.getStatus() ) )
        raise Exception(response.getStatus())
