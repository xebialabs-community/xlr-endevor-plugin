#!flask/bin/python
#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

def getFile( fileName ):
     filePath="/endevor/responses/%s" % fileName
     F = open(filePath, "r")
     resp = make_response( F.read() )
     resp.headers['Content-Type'] = 'application/json'
     return resp

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/EndevorService/rest/application.wadl')
def wadl():
     return getFile("RestAPi_endeavor.wadl")

@app.route('/EndevorService/rest/<instance>/packages', methods=['GET'])
def listPackages( instance ):
     if instance == "AETNA":
         return getFile("ListPackagesResponse-aetna.json")
     return getFile("ListPackagesResponse.json")

@app.route('/EndevorService/rest')
def listAllConfigurations():
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>')
def listConfigurationParameters( instance ):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>', methods=['POST', 'PUT'])
def createPackage(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Cast', methods=['PUT'])
def castPackage(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Approve', methods=['PUT'])
def approve( instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Execute', methods=['PUT'])
def executePackage(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Backout', methods=['PUT'])
def backoutPackag(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Commit', methods=['PUT'])
def commitPackage(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Ship', methods=['PUT'])
def shipPackage( instance, package ):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>', methods=['DELETE'])
def deletePackage(instance, package):
     return getFile("ShipPackageResponse.json")

@app.route('/EndevorService/rest/<instance>/packages/<package>/Reset', methods=['PUT'])
def resetPackage(instance, package):
     return getFile("ShipPackageResponse.json")

if __name__ == '__main__':
    app.run(debug=True)

