from dnslookup.lookup_util import dnslookup
from dnslookup.DNSLookupBase import DNSLookupBase


class DomainDNSRecord(DNSLookupBase):
    def __init__(self, name_server, records, response_time):
        DNSLookupBase.__init__(self)
        self.name_server = name_server
        self.records = records
        self.response_time = response_time


class Domain(DNSLookupBase):
    def __init__(self, url):
        DNSLookupBase.__init__(self)
        try:
            from queue import Queue
        except ImportError:
            from Queue import Queue

        self.url = url
        self.results = Queue()
        self.status = Queue()

    def lookup(self, name_server_collection):
        for key, name_server in name_server_collection.collection.items():
            ips, time = dnslookup(domain=self.url, nameserver_ip=name_server.ip)
            self.results.put(DomainDNSRecord(name_server=name_server, records=ips, response_time=time))
        self.status.put("Finished")
