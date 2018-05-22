#!flask/bin/python

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

