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

    def endevor_listallconfigurations(self, variables):
        endevorUrl = 'EndevorService/rest'
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        self.logger.error("List All Configurations Request %s" % endevorUrl)
        data = self.getJson(response)
        self.logger.error("List All Configurations Response=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Create Package Return Codes")
            data['endevorReturnCode'] = "0000"
            data['endevorReasonCode'] = "0000"
            data['endevorResult'] = ['value1', 'value2', 'value3']
            return {'output': data}
            return (data['returnCode'], data['reasonCode'], data['data'])
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_listconfigurationparameters(self, variables):
        endevorUrl = 'EndevorService/rest/%s' % variables['instance']
        response = self.httpRequest.get(endevorUrl, contentType='application/json')
        self.logger.error("List Configuration Parameters Request %s" % endevorUrl)
        data = json.loads(response.getResponse())
        self.logger.error("List Configuration Parameters Response=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            # TO-DO:  determine structure of returned data
            #           return (data.returnCode, data.reasonCode, data.data['key'])
            self.logger.error("List Configuration Parameters Return Codes")
            data['endevorReturnCode'] = "0000"
            data['endevorReasonCode'] = "0000"
            data['endevorResult'] = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_listpackages(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages' % variables['instance']

        if variables['status']:
            for item in variables['status']:
                endevorUrl = "%s&status=%s" % (endevorUrl, item)
        if variables['packageType']:
            endevorUrl = "%s&type=%s" % (endevorUrl, variables['packageType'])
        if variables['enterprise']:
            endevorUrl = "%s&enterprise=%s" % (endevorUrl, variables['enterprise'])
        if variables['promotion']:
            endevorUrl = "%s&promotion=%s" % (endevorUrl, promotion)

        self.logger.error("List Packages Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.get(endevorUrl.replace('&','?',1), contentType='application/json')
        data = json.loads(response.getResponse())
        self.logger.error("List Packages Response=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            pkgList=[]
            for pkg in data['data']:
                self.logger.info( "PKG = %s" % pkg )
                if( "pkgId" in pkg ):
                    pkgList.append( pkg['pkgId'] )
                if( "PKG ID" in pkg ):
                    pkgList.append( pkg['PKG ID'] )
            self.logger.error("List Packages Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = pkgList
            return {'output': data}
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_updatepackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (variables['instance'], variables['package'])

        if variables['description']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['description']))
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

        self.logger.error("Update Package Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = json.loads(response.getResponse())
        self.logger.error("Update Package Response=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("List Configuration Parameters Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = ""
            return {'output': data}
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
        self.logger.error("Create Package Return =============\n%s\n=============\n" % json.dumps(data, indent=4, sort_keys=True) )
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


    def endevor_castpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Cast' % (variables['instance'], variables['package'])

        if variables['ewfromdate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewfromdate']))
        if variables['ewfromtime']:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, urllib.quote(variables['ewfromtime']))
        if variables['ewtodate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewtodate']))
        if variables['ewtotime']:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, urllib.quote(variables['ewtotime']))
        if variables['validateComponents']:
            endevorUrl = "%s&validate-components=%s" % (endevorUrl, urllib.quote(variables['validateComponents']))
        if variables['backout']:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "yes")
        else:
            endevorUrl = "%s&backout=%s" % (endevorUrl, "no")

        self.logger.error("Cast Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Cast Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Cast Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_approvepackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Approve' % (variables['instance'], variables['package'])

        self.logger.error("Approve Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Approve Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Approve Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_executepackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Execute' % (variables['instance'], variables['package'])

        if variables['ewfromdate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewfromdate']))
        if variables['ewfromtime']:
            endevorUrl = "%s&ewfromtime=%s" % (endevorUrl, urllib.quote(variables['ewfromtime']))
        if variables['ewtodate']:
            endevorUrl = "%s&ewfromdate=%s" % (endevorUrl, urllib.quote(variables['ewtodate']))
        if variables['ewtotime']:
            endevorUrl = "%s&ewtotime=%s" % (endevorUrl, urllib.quote(variables['ewtotime']))
        if variables['status']:
            endevorUrl = "%s&status=%s" % (endevorUrl, urllib.quote(variables['status']))

        self.logger.error("Execute Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Execute Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Execute Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_backoutpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backout' % (variables['instance'], variables['package'])

        if variables['statement']:
            endevorUrl = "%s&statement=%s" % (endevorUrl, urllib.quote(variables['statement']))
        if variables['element']:
            endevorUrl = "%s&element=%s" % (endevorUrl, urllib.quote(variables['element']))

        self.logger.error("Backout Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Backout Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Backout Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_backinpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Backin' % (variables['instance'], variables['package'])

        if variables['statement']:
            endevorUrl = "%s&statement=%s" % (endevorUrl, urllib.quote(variables['statement']))
        if variables['element']:
            endevorUrl = "%s&element=%s" % (endevorUrl, urllib.quote(variables['element']))

        self.logger.error("Backin Package Request %s" % endevorUrl.replace('&','?',1))
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Backin Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Backin Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_commitpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Commit' % (variables['instance'], variables['package'])

        if variables['olderThan']:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, urllib.quote(variables['olderThan']))
        if variables['deletePromotionHistory']:
            endevorUrl = "%sdelete-promotion-history=%s" % (endevorUrl, "true")
        else:
            endevorUrl = "%sdelete-promotion-history=%s" % (endevorUrl, "false")

        self.logger.error("Commit Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Commit Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Commit Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_shippackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Ship' % (variables['instance'], variables['package'])

        if variables['destination']:
            endevorUrl = "%s&destination=%s" % (endevorUrl, urllib.quote(variables['destination']))
        if variables['option']:
            endevorUrl = "%s&option=%s" % (endevorUrl, urllib.quote(variables['option']))
        if variables['prefix']:
            endevorUrl = "%s&prefix=%s" % (endevorUrl, urllib.quote(variables['prefix']))

        self.logger.error("Ship Package Request %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Ship Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Ship Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_deletepackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s' % (variables['instance'], variables['package'])

        if variables['olderThan']:
            endevorUrl = "%s&olderthan=%s" % (endevorUrl, urllib.quote(variables['olderThan']))
        if variables['status']:
            endevorUrl = "%s&status=%s" % (endevorUrl, urllib.quote(variables['status']))

        self.logger.error("Delete Package %s" % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.delete(endevorUrl.replace('&','?',1), contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Delete Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Delete Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
        else:
            self.logBadReturnCodes(data)
        self.throw_error(response)

    def endevor_resetpackage(self, variables):
        endevorUrl = 'EndevorService/rest/%s/packages/%s/Reset' % (variables['instance'], variables['package'])

        self.logger.error("Reset Package Request %s " % endevorUrl.replace('&','?',1) )
        response = self.httpRequest.put(endevorUrl.replace('&','?',1), '{}', contentType='application/json')
        data = self.getJson(response)
        self.logger.error("Reset Package Return=============\n%s\n==================" % json.dumps(data, indent=4, sort_keys=True))
        if response.getStatus() in HTTP_SUCCESS:
            self.logger.error("Delete Package Return Codes")
            data['endevorReturnCode'] = data['returnCode']
            data['endevorReasonCode'] = data['reasonCode']
            data['endevorResult'] = data['messages']
            return {'output': data}
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
