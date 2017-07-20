### WSO2 Admin Services
WSO2 products are managed internally using SOAP Web services known as admin services. WSO2 products come with a management console UI, which communicates with these admin services to facilitate administration capabilities through the UI.
A service in WSO2 products is defined by the following components:
Service component: provides the actual service
UI component: provides the Web user interface to the service
Service stub: provides the interface to invoke the service generated from the service WSDL
There can be instances where you want to call back-end Web services directly. For example, in test automation, to minimize the overhead of having to change automation scripts whenever a UI change happens, developers prefer to call the underlying services in scripts. The topics below explain how to discover and invoke these services from your applications.
### Discovering the admin services
By default, the WSDLs of admin services are hidden from consumers. Given below is how to discover them.
Set the <HideAdminServiceWSDLs> element to false in the <PRODUCT_HOME>/repository/conf/carbon.xml file.
Restart the server.
Start the WSO2 product with the -DosgiConsole option, such as sh <PRODUCT_HOME>/bin/wso2server.sh -DosgiConsole in Linux.
When the server is started, hit the enter/return key several times to get the OSGI shell in the console.
In the OSGI shell, type: osgi> listAdminServices
The list of admin services of your product are listed. For example:

To see the service contract of an admin service, select the admin service's URL and then paste it in your browser with ?wsdl at the end. For example:
https://localhost:9443/services/UserAdmin?wsdl
In products like WSO2 ESB and WSO2 API Manager, the port is 8243 (assuming 0 port offset). However, you should be accessing the Admin Services via the management console port, which is 9443 when there is no port offset.
Note that the admin service's URL appears as follows in the list you discovered in step 6:
AuthenticationAdmin, AuthenticationAdmin, https://<host IP>:8243/services/AuthenticationAdmin
### Invoking an admin service
Admin services are secured using common types of security protocols such as HTTP basic authentication, WS-Security username token, and session based authentication to prevent anonymous invocations. For example, the UserAdmin Web service is secured with the HTTP basic authentication. To invoke a service, you do the following:
Authenticate yourself and get the session cookie.
Generate the client stubs to access the back-end Web services.
To generate the stubs, you can write your own client program using the Axis2 client API or use an existing tool like SoapUI (4.5.1 or later) or wsdl2java.
The wsdl2java tool, which comes with WSO2 products by default hides all the complexity and presents you with a proxy to the back-end service. The stub generation happens during the project build process within the Maven POM files. It uses the Maven ant run plug-in to execute the wsdl2java tool.
You can also use the Java client program given here to invoke admin services. All dependency JAR files that you need to run this client are found in the /lib directory.
Authenticate the user
The example code below authenticates the user and gets the session cookie:

import org.apache.axis2.AxisFault;
import org.apache.axis2.transport.http.HTTPConstants;
import org.wso2.carbon.authenticator.stub.AuthenticationAdminStub;
import org.wso2.carbon.authenticator.stub.LoginAuthenticationExceptionException;
import org.wso2.carbon.authenticator.stub.LogoutAuthenticationExceptionException;
import org.apache.axis2.context.ServiceContext;
import java.rmi.RemoteException;

public class LoginAdminServiceClient {
  private final String serviceName = "AuthenticationAdmin";
    private AuthenticationAdminStub authenticationAdminStub;
    private String endPoint;

    public LoginAdminServiceClient(String backEndUrl) throws AxisFault {
      this.endPoint = backEndUrl + "/services/" + serviceName;
      authenticationAdminStub = new AuthenticationAdminStub(endPoint);
    }

    public String authenticate(String userName, String password) throws RemoteException,
                                      LoginAuthenticationExceptionException {

      String sessionCookie = null;

      if (authenticationAdminStub.login(userName, password, "localhost")) {
        System.out.println("Login Successful");

        ServiceContext serviceContext = authenticationAdminStub.
            _getServiceClient().getLastOperationContext().getServiceContext();
        sessionCookie = (String) serviceContext.getProperty(HTTPConstants.COOKIE_STRING);
        System.out.println(sessionCookie);
      }

      return sessionCookie;
    }

    public void logOut() throws RemoteException, LogoutAuthenticationExceptionException {
      authenticationAdminStub.logout();
    }
}
To resolve dependency issues, if any, add the following dependency JARs location to the class path: <PRODUCT_HOME>/repository/components/plugins.
The the AuthenticationAdminStub class requires org.apache.axis2.context.ConfigurationContext as a parameter. You can give a null value there.
Generate the client stubs
After authenticating the user, give the retrieved admin cookie with the service endpoint URL as shown in the sample below. The service management service name is ServiceAdmin. You can find its URL (e.g., https://localhost:9443/services/ServiceAdmin) in the service.xml file in the META-INF folder in the respective bundle that you find in <PRODUCT_HOME>/repository/components/plugins.
import org.apache.axis2.AxisFault;
import org.apache.axis2.client.Options;
import org.apache.axis2.client.ServiceClient;
import org.wso2.carbon.service.mgt.stub.ServiceAdminStub;
import org.wso2.carbon.service.mgt.stub.types.carbon.ServiceMetaDataWrapper;
import java.rmi.RemoteException;

public class ServiceAdminClient {
  private final String serviceName = "ServiceAdmin";
  private ServiceAdminStub serviceAdminStub;
  private String endPoint;

  public ServiceAdminClient(String backEndUrl, String sessionCookie) throws AxisFault {
    this.endPoint = backEndUrl + "/services/" + serviceName;
    serviceAdminStub = new ServiceAdminStub(endPoint);
    //Authenticate Your stub from sessionCooke
    ServiceClient serviceClient;
    Options option;

    serviceClient = serviceAdminStub._getServiceClient();
    option = serviceClient.getOptions();
    option.setManageSession(true);
    option.setProperty(org.apache.axis2.transport.http.HTTPConstants.COOKIE_STRING, sessionCookie);
  }

  public void deleteService(String[] serviceGroup) throws RemoteException {
    serviceAdminStub.deleteServiceGroups(serviceGroup);

  }

  public ServiceMetaDataWrapper listServices() throws RemoteException {
    return serviceAdminStub.listServices("ALL", "*", 0);
  }
}
The following sample code lists the back-end Web services:
import org.wso2.carbon.authenticator.stub.LoginAuthenticationExceptionException;
import org.wso2.carbon.authenticator.stub.LogoutAuthenticationExceptionException;
import org.wso2.carbon.service.mgt.stub.types.carbon.ServiceMetaData;
import org.wso2.carbon.service.mgt.stub.types.carbon.ServiceMetaDataWrapper;

import java.rmi.RemoteException;

public class ListServices {
  public static void main(String[] args)
      throws RemoteException, LoginAuthenticationExceptionException,
          LogoutAuthenticationExceptionException {
    System.setProperty("javax.net.ssl.trustStore", "$ESB_HOME/repository/resources/security/wso2carbon.jks");
    System.setProperty("javax.net.ssl.trustStorePassword", "wso2carbon");
    System.setProperty("javax.net.ssl.trustStoreType", "JKS");
    String backEndUrl = "https://localhost:9443";

    LoginAdminServiceClient login = new LoginAdminServiceClient(backEndUrl);
    String session = login.authenticate("admin", "admin");
    ServiceAdminClient serviceAdminClient = new ServiceAdminClient(backEndUrl, session);
    ServiceMetaDataWrapper serviceList = serviceAdminClient.listServices();
    System.out.println("Service Names:");
    for (ServiceMetaData serviceData : serviceList.getServices()) {
      System.out.println(serviceData.getName());
    }

    login.logOut();
  }
}
