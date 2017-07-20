from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

session = Session()
session.verify = False
session.auth = HTTPBasicAuth('admin', 'admin')

client = Client('./wsdl/UserAdmin.xml',
                transport=Transport(session=session))

print client.service.listAllUsers('*', 100)

print client.service.listUsers('*', 100)

# print client.service.addUser('zhanlif', '123456')

print client.service.getRolesOfUser('zhanlif', '*', '100')

print client.service.getAllRolesNames('*', '100')

# print client.service.addRemoveRolesOfUser('zhanlif', None,
#                                           ['Internal/creator', 'Internal/subscriber', 'Internal/publisher'])

# print client.service.updateRolesOfUser('zhanlif', ['Internal/creator','Internal/publisher'])
