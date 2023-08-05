# encoding=utf8

from DNSLookupBase import DNSLookupBase
from NameServer import NameServer


class NameServerCollection(DNSLookupBase):
    def __init__(self):
        DNSLookupBase.__init__(self)
        self.collection = {}

    def add_server(self, name_server):
        self.collection[name_server.ip] = name_server

    @classmethod
    def CollectionFromCSV(cls, csv_data):
        import csv
        collection = cls()
        reader = csv.DictReader(csv_data)
        for row in reader:
            collection.add_server(NameServer.BuildFromCSV(csv_row=row))

        return collection

    @classmethod
    def CollectionFromCSVURL(cls, url):
        if str(url).lower().startswith("http"):
            response = cls.get_url_content(url)

        else:
            with open(url, 'r') as input_file:
                response = input_file.readlines()

        return cls.CollectionFromCSV(csv_data=response)
