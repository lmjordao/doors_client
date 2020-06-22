"""

"""
from http import cookiejar
from http.cookiejar import parse_ns_headers

import requests
import xml.etree.ElementTree as xmlET

import urllib3
from requests.cookies import create_cookie
from urllib3.exceptions import InsecureRequestWarning

from api.api_config import APIConfig
from common.common import Common


def cookie_dict(args):
    pass


class OSLCApi:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(OSLCApi, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        """
        :rtype: OSLCApi
        """
        print('__OSLCAPI__ Initialising...')
        authentication_server = APIConfig.AUTHENTICATION_SERVER
        server_address = APIConfig.SERVER_ADDRESS

        # disable Insecure Request Warning
        urllib3.disable_warnings(InsecureRequestWarning)
        # Keeps the server session data
        self.authentication_server = authentication_server
        # self.username = ServerConfig.USERNAME
        # self.password = ServerConfig.PASSWORD
        self.username = 'hdias'  # ConfigFile.getinstance().config_section_map("CCM")['login']
        self.password = 'bt12345'  # ConfigFile.getinstance().config_section_map("CCM")['passwd']
        self.session = OSLCApi.server_login(self.authentication_server, self.username,
                                            self.password)
        self.server_address = server_address
        self.service = 'ccm'

        if self.__initialized:
            return
        self.__initialized = True

        OSLCApi.register_namespaces()

    @staticmethod
    def getinstance():

        if OSLCApi.__instance is None:
            OSLCApi()

        return OSLCApi.__instance

    @staticmethod
    def get_root_services(server_address, service):
        """
        retrieves the tree for the root services. Either RM, QM or CCM
        typical URL is https://localhost:9443/rm/rootservices
        :param server_address: Server address in the format
        https://localhost:9443
        :param service: RM, QM, DWA, ...
        :return: the root services RDF+XML in ElementTree format.
        """
        root_services_link = server_address + '/' + service + '/rootservices'
        try:
            response = requests.get(root_services_link,
                                    verify=False,
                                    headers=APIConfig.GET_DEFAULT_HEADERS,
                                    proxies=[])

            print('root services: ' + str(response.content))
            root_services_tree = xmlET.ElementTree(
                xmlET.fromstring(response.content))
            root_services_root = root_services_tree.getroot()

            return root_services_root, APIConfig.OPERATION_SUCCESS

        except (requests.exceptions.ConnectionError, xmlET.ParseError,
                UnicodeEncodeError) as exception:
            print(('ERROR: Failed to retrieve or parse the root services '
                   'response. \nREASON: ' + str(exception)))
            print(('Root link: ' + str(root_services_link)))
            exit(404)

    @staticmethod
    def get_oslc_catalog(server_address, service):
        """
        retrieves the catalog link based on the root services rdf.
        :param server_address: in the format : https://localhost:9443/
        :param service: 'rm', 'qm', ...
        :return: the catalog link
        """
        root_services, error = OSLCApi.get_root_services(server_address, service)
        service_provider = None
        if service == 'rm':
            service_provider = 'xmlns_rm:rmServiceProviders'
        elif service == 'qm':
            service_provider = 'oslc_qm:qmServiceProviders'
        elif service == 'ccm':
            service_provider = 'xmlns_cm:cmServiceProviders'
        elif 'dwa' in service:
            service_provider = 'oslc_rm:rmServiceProviders'
        else:
            print(('ERROR: <' + str(service) + '> not recognized.'))
            exit(404)
        try:
            service_provider = service_provider.split(':')[0]
            print(service_provider)
            # service_provider = root_services.findx(service_provider)
            service_provider = root_services.find(service_provider, namespaces=APIConfig.OSLC_NAMESPACE_MAP)
            print('service provider: ' + str(service_provider))
            input('parei aqui 7')
            service_provider = 'http://open-services.net/ns/rm#'
        except SyntaxError as error:
            print(('ERROR: Failed to find <' + str(service_provider) + '>. \n'
                                                                       'REASON: ' + str(error)))
            exit(404)

        # oslc_catalog_link = service_provider.getx('rdf:resource')
        oslc_catalog_link = service_provider.get(Common.get_resolved_element('rdf:resource'))
        if APIConfig.DEBUG:
            print('oslc_catalog_link: ' + oslc_catalog_link)

        return oslc_catalog_link

    @staticmethod
    def server_request(operation, url, data=None, custom_headers=None, params=None, use_default_headers=True):
        """
        Shadows the 'requests' class for server requests.
        :param operation: 'GET', 'POST', 'PUT'
        :param url: target url
        :param data: data for 'PUT' or 'POST'
        :param custom_headers: define own headers if necessary
        :param params: in the case of a query
        :param use_default_headers:
        :return: the request, status if operation was valid
        """
        counter = 2  # Number of attempts to perform the request
        status_code = APIConfig.OPERATION_ERROR
        oslc_api = OSLCApi.getinstance()

        class ResponseObject:
            def __init__(self):
                self.content = None
                self.status_code = None

        response = ResponseObject()
        response.status_code = status_code
        response.content = None

        while counter > 0:
            try:
                response.status_code = status_code
                response.content = None
                if url is None:
                    return response, status_code

                if operation == 'GET':

                    if custom_headers is not None:

                        if use_default_headers:
                            headers = APIConfig.GET_DEFAULT_HEADERS.copy()
                            headers.update(custom_headers)
                        else:
                            headers = custom_headers
                    else:
                        headers = APIConfig.GET_DEFAULT_HEADERS
                    print("head", headers)
                    last_cookie = dict(OSLCApi.session.cookies)
                    # last_cookie['JSESSIONID'] = 'E0A7F14C91637F6C669D4911B8A7AC43'
                    print(last_cookie)
                    response = oslc_api.session.get(url,
                                                    headers=headers,
                                                    verify=False,
                                                    params=params, cookies=last_cookie)
                    print('novo', oslc_api.session.cookies)
                    '''response = oslc_api.session.get(url,
                                                    headers=headers,
                                                    verify=False,
                                                    params=params)'''

                if operation == 'POST':
                    #data = {'dwa_repository_value': 'urn:rational:ers-47b40ea446070b27:', 'loginButton': '','j_password': 'bt12345', 'j_username': 'hdias'}
                    print(data)
                    if data is None:
                        return response, status_code
                    else:
                        if custom_headers is not None:
                            headers = oslc_api.session.headers.copy()
                            if use_default_headers:
                                headers.update(APIConfig.POST_DEFAULT_HEADERS)
                            headers.update(custom_headers)
                        else:
                            headers = oslc_api.session.headers
                            headers.update(APIConfig.POST_DEFAULT_HEADERS)
                        response = oslc_api.session.post(url,
                                                         data=data,
                                                         headers=headers,
                                                         verify=False,
                                                         params=params)

                if operation == 'PUT':
                    if data is None:
                        return response, status_code
                    else:
                        if custom_headers is not None:
                            headers = oslc_api.session.headers.copy()
                            if use_default_headers:
                                headers.update(APIConfig.PUT_DEFAULT_HEADERS)
                            headers.update(custom_headers)
                        else:
                            headers = oslc_api.session.headers
                            updated_headers = APIConfig.PUT_DEFAULT_HEADERS.copy()
                            headers.update(updated_headers)

                        response = oslc_api.session.put(url,
                                                        data=data,
                                                        headers=headers,
                                                        verify=False,
                                                        params=params)

                if operation == 'DEL':
                    if custom_headers is not None:
                        headers = oslc_api.session.headers.copy()
                        if use_default_headers:
                            headers.update(APIConfig.PUT_DEFAULT_HEADERS)
                        headers.update(custom_headers)
                    else:
                        headers = oslc_api.session.headers
                        updated_headers = APIConfig.PUT_DEFAULT_HEADERS.copy()
                        headers.update(updated_headers)

                    response = oslc_api.session.delete(url,
                                                       headers=headers,
                                                       verify=False,
                                                       params=params)
                status_code = APIConfig.OPERATION_SUCCESS
                counter = 0  # Break while

            except requests.exceptions.ConnectionError as ex:
                oslc_api.session = OSLCApi.server_login(oslc_api.authentication_server, oslc_api.username,
                                                        oslc_api.password)
                counter -= 1
                status_code = APIConfig.OPERATION_ERROR

        return response, status_code

    @staticmethod
    def find_prefix_in_namespace_map(url):
        """
        this method shall retrieve the prefix used for a specific URL.
        Works like a backwards dict for the namespace map
        :param url: the url to search for
        :return: the namespace definition
        """

        for prefix, namespace_url in list(APIConfig.OSLC_NAMESPACE_MAP.items()):
            if namespace_url == url:
                return prefix

    @staticmethod
    def register_namespaces(key=None, namespace=None):
        """
        registers the namespaces
        :param key: new prefix to register
        :param namespace: new uri to register
        :return: nothing
        """

        for name, value in list(APIConfig.OSLC_NAMESPACE_MAP.items()):
            xmlET.register_namespace(name, value)

        if key is not None and namespace is not None:
            xmlET.register_namespace(key, namespace)

    @staticmethod
    def server_login(authentication_server, username, password):
        """
        This function shall handle the server login
        Currently not working properly. Until then, use the TOKEN0 and
        TOKEN_SECRET
        :param authentication_server: Server address that handles the login
        in the format https://localhost:9443/
        :param username: username
        :param password: password
        :return: the session data OslcApi.session
        """
        print('OSLCAPI.server_login: Authenticating...')
        OSLCApi.session = requests.Session()
        OSLCApi.session.auth = (username, password)
        authentication_link = authentication_server
        response_content = ''
        response = ''

        try:
            response = OSLCApi.session.get(authentication_link,
                                           verify=False)
            response_content = response.content
            if response.status_code != APIConfig.OPERATION_SUCCESS:
                print()
                print(('!ERROR! Server response: ' + response.status_code))
                print(response_content)
                exit(response.status_code)
        except requests.exceptions.ConnectionError as e:
            print()
            print(('!ERROR! Server response: ' + str(e)))
            print(response_content)
            exit(404)

        try:
            response = OSLCApi.session.get(authentication_link + '/auth/authrequired',
                                           verify=False, )

            response_content = response.content
            if response.status_code != APIConfig.OPERATION_SUCCESS:
                print()
                print(('!ERROR! Server response: ' + response.status_code))
                print(response_content)
                exit(response.status_code)
        except requests.exceptions.ConnectionError as e:
            print()
            print(('!ERROR! Server response: ' + str(e)))
            print(response_content)
            exit(404)

        try:
            url = response.url
            response = OSLCApi.session.get(url,
                                           verify=False)
            if response.status_code != APIConfig.OPERATION_SUCCESS:
                print()
                print(('!ERROR! Server response: ' + response.status_code))
                print(response_content)
                exit(response.status_code)
        except requests.exceptions.ConnectionError as e:
            print()
            print(('!ERROR! Server response: ' + str(e)))
            print(response_content)
            exit(404)

        try:
            url = authentication_link + APIConfig.AUTH_URL_SUFFIX
            data = {'j_username': username,
                    'j_password': password}

            login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                             'Upgrade-Insecure-Requests': '1',
                             'Accept': 'application/rdf+xml'}

            response = OSLCApi.session.post(url,
                                            data=data,
                                            verify=False,
                                            headers=login_headers)

            if response.status_code != APIConfig.OPERATION_SUCCESS:
                print()
                print(('!ERROR! Server response: ' + str(response.status_code)))
                print(response_content)
                exit(response.status_code)
            else:
                print('Authenticated as: ' + username)
        except requests.exceptions.ConnectionError as ex:
            print()
            print(('!ERROR! Server response: ' + str(ex)))
            print(response_content)
            exit(404)

        return OSLCApi.session

    @staticmethod
    def retrieve_namespace(property_definition):
        """
        retrieves the namespace and property ID from the property definition link
        :param property_definition:
        :return:
        """
        index = property_definition.rfind('#')
        if index != -1:
            namespace = property_definition[0:index + 1]
            prop = property_definition[index + 1:]
        else:
            index = property_definition.rfind('/')
            namespace = property_definition[0:index + 1]
            prop = property_definition[index + 1:]
        return namespace, prop
