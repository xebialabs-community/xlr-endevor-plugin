#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from endevor.EndevorClient import Endevor_Client

class Endevor_Client_Util(object):

    @staticmethod
    def create_endevor_client(container, username, password):
        print "Executing create_endevor_client() in Endevor_Client_Util class in EndevorClientUtil.py\n"
        return Endevor_Client.create_client(container, username, password)

