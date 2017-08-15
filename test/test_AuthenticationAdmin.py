from requests import Session
from zeep import Client
from zeep.transports import Transport

session = Session()
session.verify = False

client = Client('https://10.16.118.52:9443/services/AuthenticationAdmin?wsdl',
                transport=Transport(session=session))

# client = Client('../wsdl/AuthenticationAdmin.xml',
#                 transport=Transport(session=session))

service = client.create_service('{http://authentication.services.core.carbon.wso2.org}AuthenticationAdminSoap11Binding',
                                'https://10.16.118.52:9443/services/AuthenticationAdmin')

print service.login('admin', 'admin', 'localhost')

# print client.service.login('admin', 'admin', 'localhost')

# print client.service.login('zhanlif', '123456', 'localhost')

