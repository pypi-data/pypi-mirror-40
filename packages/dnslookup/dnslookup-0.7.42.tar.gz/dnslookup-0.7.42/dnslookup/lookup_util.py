#!/usr/bin/env python
import subprocess as sp
import sys
import re
import time
import os

nslookup_regex = re.compile(r"(Address):(\t| )?(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$")
ip_address = re.compile('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')

def dnslookup(domain, nameserver_ip):

    import dns.resolver
    result = []
    qname = dns.name.from_text(domain)
    q = dns.message.make_query(qname, dns.rdatatype.A)
    start = time.time()
    r = dns.query.udp(q, nameserver_ip)
    end = time.time()
    for answers in r.answer:
        for answer in answers:
            result.append(str(answer))
    return result, end-start



def nslookup(domain, nameserver_ip):
    try:

        command = "nslookup"
        start = time.time()
        process = sp.Popen([command, domain, nameserver_ip], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=False)
        end = time.time()

        (stdout, stdin, stderr) = (process.stdout, process.stdin, process.stderr)
        data = stdout.readlines()
        data = ''.join(data).split()

        if os.name != 'nt':
            answer = data.index("answer:")
            data = data[answer:]
            index = data.index("Address:")
            data = data[index+1: ]
        else:
            data = data[data.index("Addresses:") + 1:]

        ips = ''.join(data[index:])
        ips = []
        for response in data:
            match = ip_address.search(response)
            if match:
                try:
                    ips.append(match.groups(1)[0])
                except IndexError:
                    pass  # We don't care if we cant get some of the ips, but this really should happen
        return list(set(ips)), end - start

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)


if __name__ == '__main__':
    result = nslookup("google.com", "8.8.8.8")
    print(result)
    result = dnslookup("google.com", "8.8.8.8")
    print(result)
