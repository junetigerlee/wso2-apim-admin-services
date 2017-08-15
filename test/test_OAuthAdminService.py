from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

session = Session()
session.verify = False
session.auth = HTTPBasicAuth('admin', 'admin')


client = Client('https://10.16.118.52:9443/services/OAuthAdminService?wsdl',
                transport=Transport(session=session))

# client = Client('../wsdl/UserAdmin.xml',
#                 transport=Transport(session=session))

service = client.create_service('{http://oauth.identity.carbon.wso2.org}OAuthAdminServiceSoap12Binding',
                                'https://10.16.118.52:9443/services/OAuthAdminService')


print service.getOAuthApplicationData('Zeg1bfg1pkVjp5YvMe5GquKSvJUa')


print service.getOAuthApplicationDataByAppName('admin_tetet_PRODUCTION')
