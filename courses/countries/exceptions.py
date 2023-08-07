class CountriesException(Exception):
    pass


class CountriesNotFound(CountriesException):
    pass


class CountryNotExist(CountriesException):
    pass


class CountryBlockNotExist(CountriesException):
    pass
