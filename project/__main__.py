"""

"""
import csv

from api.oslc_api import OSLCApi
from doors.config import DoorsConfig


def main():
    link1 ='https://doorsdwa.bt.bombardier.net:8443/dwa/rm/discovery/service/urn:rational:ers-47b40ea446070b27:1-47b40ea446070b27-M-00255087'
    link = "https://doorsdwa.bt.bombardier.net:8443/dwa/j_acegi_security_check"
    OSLCApi()
    print(OSLCApi.session.cookies)
    print('keys', OSLCApi.session.cookies.keys())
    print(OSLCApi.session.headers)
    print('passagem')
    #input('stop, change cookie')
    '''response, op_status = OSLCApi.server_request('POST', link)
    print(response.cookies)
    print(response.content)
    print("corpo", response.history[0].request.body)'''
    response, op_status = OSLCApi.server_request('GET', link1)
    print(response.content)
    print(response.cookies)
    #print(response.headers)
    #OSLCApi.get_root_services(
     #   DoorsConfig.DOORS_SERVER_ADDRESS,
      #  DoorsConfig.DOORS_SERVICE)

    #OSLCApi.get_oslc_catalog(
      #  DoorsConfig.DOORS_SERVER_ADDRESS,
     #   DoorsConfig.DOORS_SERVICE)


if __name__ == "__main__":
    main()
