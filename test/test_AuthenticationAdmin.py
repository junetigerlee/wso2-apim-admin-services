from requests import Session
from zeep import Client
from zeep.transports import Transport

session = Session()
session.verify = False

client = Client('./wsdl/AuthenticationAdmin.xml',
                transport=Transport(session=session))

print client.service.login('admin', 'admin', 'localhost')

