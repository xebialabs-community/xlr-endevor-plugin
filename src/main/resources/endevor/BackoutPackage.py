#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from endevor.EndevorClientUtil import Endevor_Client_Util

print "Executing BackoutPackage.py"

if endevorServer is None:
  print "No server provided"
  sys.exit(1)

credentials = CredentialsFallback(endevorServer, username, password).getCredentials()

endevorClient = Endevor_Client_Util.create_endevor_client(endevorServer, credentials['username'], credentials['password'])

(endevorReturnCode, endevorReasonCode, endevorResult) = endevorClient.backout_package(instance, package, statement, element)
print endevorResult
