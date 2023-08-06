'''
Project:    CVE ID Search Utility
Author:     Sujit Ghosal
Email:      thesujit [at] gmail [dot] com
Release:    1.0 (01/17/2019)
Reqs:       * Python 3.x
            * requests
            * termcolor
            * ujson (optional, but recommended)
Disclaimer:
    Please, use this tool at your own risk! The author (Sujit Ghosal)
    shall not be responsible for any misuse done through usage of this
    tool. Any actions and or activities related to this tool is solely
    your responsibility. The misuse of this tool might result in criminal
    charges brought against the persons in question. Please pay respect
    to the third-party website owners and bandwidth, who makes these type
    of structured information available easily to the public.
'''

import argparse
from termcolor import colored
from re import findall

try:
    from ujson import loads
except ImportError as err:
    print('[+]Info: {}'.format(err))
    print('[*]Falls back to, json built-in')
    from json import loads

def find_cve_data(cve):
    '''
    Find the available information for a particular CVE from Metasploit,
    ExploitDB, Misc References and Bugtraq etc. Once the information has
    been retrieved, STDOUT all matches.
    '''
    from requests import get

    host = "http://cve.circl.lu/api/cve/CVE-"
    agent = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64; rv:58.0)Gecko/20100101 Firefox/58.0"
    }

    # Perform web requests for via API endpoint
    http_obj = get(host + cve, headers=agent, timeout=4)

    if http_obj.json():
        json_obj = loads(http_obj.text.encode('ascii', 'utf-8'))
        print(colored('Vulnerability Description:\n' + '=' * 27,
                      'yellow'))
        print(json_obj['summary'])

        ref_ps = set()
        ref_edb = set()
        ref_misc = set()
        ref_bid = set()
        ref_msf = {}

        # Enumerate sources as per reference type
        # Packetstorm
        if 'packetstorm' in json_obj:
            print(colored('Source:\tPackstorm', 'green'))
            for idx_ps in json_obj['packetstorm']:
                for each_ref in idx_ps['source']:
                    ref_ps.add(idx_ps['source'])
            for i in sorted(ref_ps):
                print("\t* " + i)

        # Exploit-DB
        if 'exploit-db' in json_obj:
            print(colored('Source:\tExploit-DB', 'green'))
            for idx_edb in json_obj['exploit-db']:
                if 'source' in idx_edb:
                    ref_edb.add(idx_edb['source'])
                if 'source' not in idx_edb and 'id' in idx_edb:
                    ref_edb.add(idx_edb['id'])
                else:
                    pass
            if len(ref_edb) > 0:
                for j in sorted(ref_edb):
                    print("\t* " + j)

        # Metasploit
        if 'metasploit' in json_obj:
            print(colored('Source:\tMetasploit', 'green'))
            for idx_msf in json_obj['metasploit']:
                if 'source' in idx_msf:
                    ref_msf[idx_msf['id']] = idx_msf['source']
                else:
                    pass
            if len(ref_msf) > 0:
                for k, v in ref_msf.items():
                    print("\t* ID:\t" + k + '\n' + "\t  URL:\t" + v)

        # Microsoft Bulletin
        if 'msbulletin' in json_obj:
            print(colored('Source:\tMicrosoft', 'green'))
            for idx_msb in json_obj['msbulletin']:
                if 'bulletin_id' in idx_msb:
                    print("\t* MSB:" + '\t' + idx_msb['bulletin_id'])
                if 'bulletin_id' not in idx_msb and 'cves_url' in idx_msb:
                    print("\t* URL: " + '\t' + idx_msb['cves_url'])
                else:
                    pass

        # Bugtraq (SecurityFocus) / Testcase: 2010-1042
        if 'refmap' in json_obj:
            for idx_refmaps in json_obj['refmap'].items():
                refmap, ids = idx_refmaps   # Unpack tuple
                for x in range(0, len(refmap)):
                    if refmap == 'bid':
                        ref_bid.add(ids[0])

            if len(ref_bid) > 0:
                print(colored('Source:\tSecurityFocus', 'green'))
                for each_bugid in ref_bid:
                    print("\t* ID:" + '\t' + each_bugid)

        # Misc. References
        if 'references' in json_obj:
            print(colored('Source:\tMisc', 'green'))
            for idx_misc in json_obj['references']:
                ref_misc.add(idx_misc)
            if len(ref_misc) > 0:
                for m in sorted(ref_misc):
                    print("\t* " + m)
    else:
        print(colored('[-]No matches found!\n', 'red'))

    print


def main():
    parser = argparse.ArgumentParser(description="-[[ CVE Search Utility ]]-")
    parser.add_argument('-s', '--search', dest='cve_id', required=True,
                        type=str, help='CVE ID, e.g: 2017-0145')
    args = parser.parse_args()

    # Validate CVE input string
    if len(findall('^\d{4}\-\d{4,8}$', args.cve_id)) > 0:
        find_cve_data(args.cve_id)
    else:
        print(colored('[-]Invalid CVE format input!\n', 'red'))
        parser.print_help()
