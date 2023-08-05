#!/usr/bin/env python
import sys
import os
from prettytable import PrettyTable
from IPy import IP

sys.path.insert(0, os.path.dirname(__file__))

from lib.nmap import PortScanner

class Output():
    def __init__(self, filename):
        self.filename = filename
    
    def excel(self, headers, rows):
        from xlwt import Workbook
        outbook = Workbook()
        for i in rows:
            worksheet = outbook.add_sheet(i)
            for col in headers:
                worksheet.write(0, headers.index(col), col)
            count=1
            for x in rows[i]:
                for col in headers:
                    worksheet.write(count, headers.index(col), x[col])
                count += 1
        outbook.save(self.filename)

def source_scan(source):
    output = []
    agent = PortScanner()
    agent.scan(source, arguments="-sP")

    iplist = [(IP(ip).int(), ip) for ip in agent.all_hosts()]
    iplist.sort()
    
    for x,y in iplist:
        agent[y]["addresses"].setdefault('ipv4', '')
        agent[y]["addresses"].setdefault('ipv6', '')
        agent[y]["addresses"].setdefault('mac', '')
        output.append({'hostname':agent[y]["hostname"],
                       'ipv4':agent[y]["addresses"]['ipv4'],
                       'ipv6':agent[y]["addresses"]['ipv6'],
                       'mac':agent[y]["addresses"]['mac']})
    return output

def display_output(headers, rows):
    table = PrettyTable(headers)
    table.align = "l"
    for i in rows:
        for x in rows[i]:
            table.add_row([x[o] for o in headers])
    print (table)

def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [action] [options]",
                          version="%prog 0.0.1")
    parser.add_option("-f", "--fields", dest="fields",
                      default="ipv4,mac,hostname",
                      help="Display fields (ip, name, type).")
    parser.add_option("-o","--output", dest="output", default=None,
                      help="Output format:filename (default=stdout).",
                      type="string")
    parser.add_option("-s","--sources", dest="sources",default=None,
                      help="Update domain list.",type="string")

    (options, args) = parser.parse_args()
    if options.sources:
        hostfound = {}
        for i in options.sources.split(","):
            hostfound[i] = source_scan(i)
            
        if options.output is None:
            display_output(options.fields.split(","), hostfound)
        else:
            output = Output(options.output)
            output.excel(options.fields.split(","), hostfound)
    else:
        print("Required arguments missing or invalid.")
        print(parser.print_help())
        sys.exit(-1)

if __name__ == '__main__':
    main()
