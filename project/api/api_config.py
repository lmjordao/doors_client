"""

"""
from doors.config import DoorsConfig


class APIConfig:

    AUTHENTICATION_SERVER = DoorsConfig.DOORS_AUTH_SERVER
    SERVER_ADDRESS = DoorsConfig.DOORS_SERVER_ADDRESS

    #AUTHENTICATION_SERVER = DoorsConfig.DOORS_AUTH_SERVER
    #SERVER_ADDRESS = DoorsConfig.DOORS_SERVER_ADDRESS

    AUTH_URL_SUFFIX = '/auth/j_security_check'
    DEBUG = True

    OPERATION_SUCCESS = 200
    OPERATION_ERROR = 500
    HEADER = {'accept': 'application/rdf+xml'}
    GET_DEFAULT_HEADERS = {'OSLC-Core-Version': '2.0',
                           'Accept': 'application/rdf+xml'}
    PUT_DEFAULT_HEADERS = {'OSLC-Core-Version': '2.0',
                           'Accept': 'application/rdf+xml',
                           'Content-Type': 'application/rdf+xml'}
    POST_DEFAULT_HEADERS = {'OSLC-Core-Version': '2.0',
                            'Accept': 'application/rdf+xml',
                            'Content-Type': 'application/rdf+xml'}
    OSLC_NAMESPACE_MAP = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                          'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                          'dc': 'http://purl.org/dc/terms/',
                          'oslc': 'http://open-services.net/ns/core#',
                          'rm': 'http://www.ibm.com/xmlns/rdm/rdf/',
                          'xmlns_rm': 'http://open-services.net/xmlns/rm/1.0/',
                          'oslc_config': 'http://open-services.net/ns/config#',
                          'qm_rqm': 'http://jazz.net/ns/qm/rqm#',
                          'oslc_qm': 'http://open-services.net/xmlns/qm/1.0/',
                          'oslc_qm_ns': 'http://open-services.net/ns/qm#',
                          'xmlns_cm': 'http://open-services.net/xmlns/cm/1.0/',
                          'oslc_cm': 'http://open-services.net/ns/cm#',
                          'oslc_disc': 'http://open-services.net/xmlns/discovery/1.0/',
                          'namespace': 'http://www.w3.org/XML/1998/namespace',
                          'dc_elements': 'http://purl.org/dc/elements/1.1/',
                          'alm': 'http://jazz.net/xmlns/alm/v0.1/',
                          'alm_qm': 'http://jazz.net/xmlns/alm/qm/v0.1/',
                          'testscript': 'http://jazz.net/xmlns/alm/qm/v0.1/testscript/v0.1/',
                          'xhtml1999': 'http://www.w3.org/1999/xhtml',
                          'rtc_ext': 'http://jazz.net/xmlns/prod/jazz/rtc/ext/1.0/',
                          'myns': 'http://mydomain.net/some/custom/namespace/v0.1/',
                          'oslc_rm': 'http://open-services.net/ns/rm#',
                          'atom': 'http://www.w3.org/2005/Atom',
                          'BTattr': 'http://rail.bombardier.com/xmlns/rm/attr/',
                          'rtc_cm': 'http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/',
                          'oslc_cmx': 'http://open-services.net/ns/cm-x#',
                          'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                          'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                          'jazzns_rm': 'http://jazz.net/ns/rm#',
                          'BTlinks': 'http://rail.bombardier.com/xmlns/rm/linktypes/',
                          'BTinks': 'http://rail.bombardier.com/xmlns/rm/linkypes/',
                          'rdm_types': 'http://www.ibm.com/xmlns/rdm/types/',
                          'nav': 'http://jazz.net/ns/rm/navigation#',
                          'jd': 'http://jazz.net/xmlns/prod/jazz/discovery/1.0/',
                          'jp06': 'http://jazz.net/xmlns/prod/jazz/process/0.6/',
                          'process': 'http://jazz.net/ns/process#',
                          'public_rm_10': 'http://www.ibm.com/xmlns/rm/public/1.0/',
                          'restDTO': 'com.ibm.team.workitem.rest.dto',
                          'queryDTO': 'com.ibm.team.workitem.query.rest.dto',
                          'trs': 'http://jazz.net/ns/trs#',
                          'jfs': 'http://jazz.net/xmlns/prod/jazz/jfs/1.0/'}
