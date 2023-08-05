#!/usr/bin/env python
import dns.query
import dns.zone
import dns.resolver
import random
import re
import sys

class DNSQuery():
    def __init__(self, server):
        self._Server = server

    def get_zone(self, domain):
        try:
            zone = dns.zone.from_xfr(dns.query.xfr("%s" %(self._Server),
                                                   "%s" %(domain)))
        except:
            print("Zone doesn't found.")
            exit(1)
        records = sorted(zone.nodes.keys())
        return zone, records

    def get_records(self, **kwargs):
        kwargs.setdefault('regex', '.*')
        kwargs.setdefault('type', ['A', 'CNAME'])

        filter_hostname = re.compile(kwargs['regex'], re.IGNORECASE)

        zone, records = self.get_zone(kwargs['domain'])
        result = []
        for i in records:
            for x in zone[i].to_text(i).split("\n"):
                row = x.split(" ")
                if (kwargs['type'] == "*") or (row[3] in kwargs['type']):
                    hostname = '.'.join([row[0], kwargs['domain']])
                    if filter_hostname.match(hostname):
                        result.append({
                            'ip': row[4],
                            'host': hostname,
                            'type': row[3],
                            'ttl': row[1]
                        })
        return result
                
    def display_output(self, records, options, delimiter):
        base_string = delimiter.join(["%(" + o + ")s" for o in options])
        for d in records:
            for o in options: d.setdefault(o, "")
            print(base_string % d)

            
def get_default_resolver(attr):
    default = dns.resolver.get_default_resolver()
    if attr == 'nameserver':
        if default.nameservers:
            return default.nameservers[0] if not default.rotate else random.choice(default.nameservers)
    elif attr == 'domain':
        dom = default.domain.to_text()[:-1]
        if not dom or dom == 'local.':
            dom = default.search[0].to_text()[:-1] if default.search else None
        return dom
    return None


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--domain", dest="domain", default=None,
                      help="Specify the domain.", metavar="str")
    parser.add_option("-f", "--fields", dest="fields", default="ip,host",
                      help="Display fields (ip, name, type).",
                      metavar="list")
    parser.add_option("-r", "--regex", dest='regex', default='.*',
                      help="Regular Expression.", metavar="str")
    parser.add_option("-s", "--server", dest="server", default=None,
                      help="DNS Server", metavar="str")
    parser.add_option("-t", "--type", dest="rtype", default="A,CNAME",
                      help="Type filter", metavar="list")
    parser.add_option("-D", "--delimiter", dest="delimiter", default="\t",
                      help="Delimiter", metavar="str")
    (options, args) = parser.parse_args()

    server = options.server if options.server else get_default_resolver('nameserver')
    domain = options.domain if options.domain else get_default_resolver('domain')
    if domain and server:
        options = {
            'server': server, 'domain': domain,
            'type': [t.upper() for t in options.rtype.split(",")],
            'regex': options.regex,
            'delimiter': options.delimiter,
            'fields': [f.lower() for f in options.fields.split(",")]
        }
        DNSAdmin = DNSQuery(options['server'])
        Records = DNSAdmin.get_records(**options)
        DNSAdmin.display_output(Records, options['fields'], 
                                options['delimiter'])
    else:
        print("DNSQuery: Required arguments missing or invalid.")
        print(parser.print_help())
        sys.exit(-1)

if __name__ == '__main__':
    main()
