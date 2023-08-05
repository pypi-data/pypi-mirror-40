import sys


class DNSLookupBase:
    def __init__(self):
        pass

    @classmethod
    def is_python3(cls):
        if int(sys.version[0]) >= 3:
            return True
        else:
            return False

    @classmethod
    def get_url_content(cls, url):
        try:
            from urllib import request
            this_response = request.urlopen(url)
            this_response = [item.decode("utf-8") for item in this_response]
        except ImportError:
            from urllib import urlopen
            this_response = urlopen(url).readlines()
        finally:
            return this_response
