"""

"""
from app.api.oslc_api import OSLCApi
from app.doors.config import DoorsConfig


def main():

    OSLCApi()

    #OSLCApi.get_root_services(
     #   DoorsConfig.DOORS_SERVER_ADDRESS,
      #  DoorsConfig.DOORS_SERVICE)

    OSLCApi.get_oslc_catalog(
        DoorsConfig.DOORS_SERVER_ADDRESS,
        DoorsConfig.DOORS_SERVICE)


if __name__ == "__main__":
    main()
