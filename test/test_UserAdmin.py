from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

session = Session()
session.verify = False
session.auth = HTTPBasicAuth('admin', 'admin')


client = Client('https://10.16.118.52:9443/services/UserAdmin?wsdl',
                transport=Transport(session=session))

# client = Client('../wsdl/UserAdmin.xml',
#                 transport=Transport(session=session))

service = client.create_service('{http://mgt.user.carbon.wso2.org}UserAdminSoap11Binding',
                                'https://10.16.118.52:9443/services/UserAdmin')

# print client.service.listAllUsers('*', 100)

print service.listAllUsers('*', 100)

# print client.service.listUsers('*', 100)

print service.listUsers('*', 100)
# print client.service.addUser('zhanlif', '123456')

# print client.service.getRolesOfUser('zhanlif', '*', '100')
print service.getRolesOfUser('zhanlif', '*', '100')
# print client.service.getAllRolesNames('*', '100')

print service.getAllRolesNames('*', '100')
# print client.service.addRemoveRolesOfUser('zhanlif', None,
#                                           ['Internal/creator', 'Internal/subscriber', 'Internal/publisher'])

# print client.service.updateRolesOfUser('zhanlif', ['Internal/creator','Internal/publisher'])
