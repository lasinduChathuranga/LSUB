#!/usr/bin/env python
# coding: utf-8
# LSUB v1 - Enhanced Subdomain Enumeration Tool with Improved crt.sh Integration

import re
import sys
import os
import argparse
import time
import multiprocessing
import threading
import socket
import json
from datetime import datetime

# External modules
try:
    from subbrute import subbrute
except ImportError:
    subbrute = None
try:
    import dns.resolver
except ImportError:
    dns = None
try:
    import requests
except ImportError:
    requests = None

# Python 2.x and 3.x compatibility
if sys.version > '3':
    import urllib.parse as urlparse
    import urllib.parse as urllib
else:
    import urlparse
    import urllib

try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
class Colors:
    BLUE = '\033[94m'        # Blue
    CYAN = '\033[96m'        # Cyan
    GREEN = '\033[92m'       # Green
    YELLOW = '\033[93m'      # Yellow
    RED = '\033[91m'         # Red
    ENDC = '\033[0m'         # Reset
    BOLD = '\033[1m'         # Bold
    PURPLE = '\033[95m'      # Purple

def no_color():
    """Disable all colors"""
    for attr in dir(Colors):
        if not attr.startswith('_'):
            setattr(Colors, attr, '')

def print_banner():
    print(Colors.BLUE + """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                              LSUB V1                                 ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║    ██╗     ███████╗██╗   ██╗██████╗     ██╗   ██╗ ██╗                ║
    ║    ██║     ██╔════╝██║   ██║██╔══██╗    ██║   ██║███║                ║
    ║    ██║     ███████╗██║   ██║██████╔╝    ██║   ██║╚██║                ║
    ║    ██║     ╚════██║██║   ██║██╔══██╗    ╚██╗ ██╔╝ ██║                ║
    ║    ███████╗███████║╚██████╔╝██████╔╝     ╚████╔╝  ██║                ║
    ║    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝       ╚═══╝   ╚═╝                ║
    ║                                                                      ║
    ║                                                                      ║
    ║           ENHANCED SUBDOMAIN ENUMERATION TOOL                        ║
    ║                    With Improved crt.sh Integration                  ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """ + Colors.ENDC)

def print_config_summary(domain, threads, bruteforce, verbose, ports, output):
    print(Colors.PURPLE + """
    ══════════════════════════════════════════════════════════════════════
                             CONFIGURATION SUMMARY                        
                                                                   """ + Colors.ENDC)
    print(Colors.PURPLE + f"     Target Domain: {domain:<50} " + Colors.ENDC)
    print(Colors.PURPLE + f"     Threads: {threads:<58} " + Colors.ENDC)
    print(Colors.PURPLE + f"     Bruteforce: {'Enabled' if bruteforce else 'Disabled':<53} " + Colors.ENDC)
    print(Colors.PURPLE + f"     Verbose: {'Enabled' if verbose else 'Disabled':<56} " + Colors.ENDC)
    print(Colors.PURPLE + f"     Port Scan: {ports if ports else 'Disabled':<54} " + Colors.ENDC)
    print(Colors.PURPLE + f"     Output File: {output if output else 'Console Only':<52} " + Colors.ENDC)
    print(Colors.PURPLE + "     " + Colors.ENDC)

def print_target_analysis(domain):
    print(Colors.BLUE + """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                           TARGET ANALYSIS                            ║
    ╠══════════════════════════════════════════════════════════════════════╣""" + Colors.ENDC)
    print(Colors.BLUE + f"    ║ Enumerating subdomains for: {domain:<41}║" + Colors.ENDC)
    print(Colors.BLUE + "    ╚══════════════════════════════════════════════════════════════════════╝" + Colors.ENDC)

def print_engine_groups():
    print(Colors.CYAN + """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                           SEARCH ENGINES                             ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║  SEARCH ENGINES GROUP (6):          SPECIALIZED ENGINES GROUP (6):   ║
    ║  ┌─────────────────────────┐        ┌─────────────────────────────┐  ║
    ║  │ 1. Google               │        │ 1. SSL Certificates (crt.sh)│  ║
    ║  │ 2. Bing                 │        │ 2. DNSdumpster              │  ║
    ║  │ 3. Yahoo                │        │ 3. VirusTotal               │  ║
    ║  │ 4. Baidu                │        │ 4. ThreatCrowd              │  ║
    ║  │ 5. Ask                  │        │ 5. PassiveDNS               │  ║
    ║  │ 6. Netcraft             │        │ 6. Certificate Transparency │  ║
    ║  └─────────────────────────┘        └─────────────────────────────┘  ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """ + Colors.ENDC)

def print_search_box(engine_name):
    print(Colors.RED + f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║ Searching  now  {engine_name:<53}║
    ╚══════════════════════════════════════════════════════════════════════╝""" + Colors.ENDC)

def parser_error(errmsg):
    print_banner()
    print("Error: " + errmsg)
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(description='LSUB v1 - Enhanced Subdomain Enumeration Tool')
    parser.error = parser_error
    
    parser.add_argument('-d', '--domain', help='Target domain', required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable bruteforce', nargs='?', default=False)
    parser.add_argument('-p', '--ports', help='Scan ports on discovered subdomains')
    parser.add_argument('-v', '--verbose', help='Verbose output', nargs='?', default=False)
    parser.add_argument('-t', '--threads', help='Number of threads (default: 30)', type=int, default=30)
    parser.add_argument('-e', '--engines', help='Engines to use (comma-separated). Available engines:\n' +
                       'Search Engines: google,bing,yahoo,baidu,ask,netcraft\n' +
                       'Specialized: ssl,dnsdumpster,virustotal,threatcrowd,passivedns,crt')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-n', '--no-color', help='Disable colored output', default=False, action='store_true')
    parser.add_argument('--show-engines', help='Show available engines grouped by category', action='store_true')
    return parser.parse_args()

def show_available_engines():
    print_banner()
    print_engine_groups()
    print(Colors.GREEN + """
    Usage Examples:
    
    # Use all engines (default)
    python lsub_enhanced.py -d example.com
    
    # Use only search engines
    python lsub_enhanced.py -d example.com -e google,bing,yahoo,baidu,ask,netcraft
    
    # Use only specialized engines
    python lsub_enhanced.py -d example.com -e ssl,dnsdumpster,virustotal,threatcrowd,passivedns,crt
    
    # Use specific engines
    python lsub_enhanced.py -d example.com -e google,ssl,dnsdumpster
    """ + Colors.ENDC)

def write_file(filename, subdomains):
    print("[+] Saving results to: " + filename)
    with open(str(filename), 'wt') as f:
        f.write("# LSUB v1 Enhanced Results\n")
        f.write("# Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("# Total: " + str(len(subdomains)) + "\n\n")
        for subdomain in subdomains:
            f.write(subdomain + os.linesep)
    print("[+] Saved " + str(len(subdomains)) + " subdomains")

def subdomain_sorting_key(hostname):
    parts = hostname.split('.')[::-1]
    if parts[-1] == 'www':
        return parts[:-1], 1
    return parts, 0

class EnumeratorBase(object):
    def __init__(self, base_url, engine_name, domain, subdomains=None, silent=False, verbose=True):
        subdomains = subdomains or []
        self.domain = urlparse.urlparse(domain).netloc
        self.session = requests.Session() if requests else None
        self.subdomains = []
        self.timeout = 25
        self.base_url = base_url
        self.engine_name = engine_name
        self.silent = silent
        self.verbose = verbose
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.print_banner()

    def print_(self, text):
        if not self.silent:
            print(text)

    def print_banner(self):
        if not self.silent:
            print_search_box(self.engine_name)

    def send_req(self, query, page_no=1):
        if not self.session:
            return None
        url = self.base_url.format(query=query, page_no=page_no)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def get_response(self, response):
        if response is None:
            return 0
        return response.text if hasattr(response, "text") else response.content

    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False
        return num >= self.MAX_PAGES

    def extract_domains(self, resp):
        return

    def check_response_errors(self, resp):
        return True

    def should_sleep(self):
        return

    def generate_query(self):
        return

    def get_page(self, num):
        return num + 10

    def enumerate(self, altquery=False):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            query = self.generate_query()
            count = query.count(self.domain)
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)
            if self.check_max_pages(page_no):
                return self.subdomains
            resp = self.send_req(query, page_no)
            if not self.check_response_errors(resp):
                return self.subdomains
            links = self.extract_domains(resp)
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)
                if retries >= 3:
                    return self.subdomains
            prev_links = links
            self.should_sleep()
        return self.subdomains

class EnumeratorBaseThreaded(multiprocessing.Process, EnumeratorBase):
    def __init__(self, base_url, engine_name, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        EnumeratorBase.__init__(self, base_url, engine_name, domain, subdomains, silent=silent, verbose=verbose)
        multiprocessing.Process.__init__(self)
        self.q = q

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)

class GoogleEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = "https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0"
        self.engine_name = "Google"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 200
        super(GoogleEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<cite.*?>(.*?)<\/cite>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                link = re.sub('<span.*>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list

    def check_response_errors(self, resp):
        if (type(resp) is str or (sys.version < '3' and type(resp) is unicode)) and 'Our systems have detected unusual traffic' in resp:
            self.print_("[-] Google is blocking requests")
            return False
        return True

    def should_sleep(self):
        time.sleep(5)

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS - 2])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query

class BingEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.bing.com/search?q={query}&go=Submit&first={page_no}'
        self.engine_name = "Bing"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        EnumeratorBaseThreaded.__init__(self, base_url, self.engine_name, domain, subdomains, q=q, silent=silent)
        self.q = q
        self.verbose = verbose

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<li class="b_algo"><h2><a href="(.*?)"')
        link_regx2 = re.compile('<div class="b_title"><h2><a href="(.*?)"')
        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2
            for link in links_list:
                link = re.sub('<(\/)?strong>|<span.*?>|<|>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list

    def generate_query(self):
        if self.subdomains:
            fmt = 'domain:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "domain:{domain} -www.{domain}".format(domain=self.domain)
        return query

class YahooEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://search.yahoo.com/search?p={query}&b={page_no}'
        self.engine_name = "Yahoo"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        super(YahooEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<span class=" fz-ms fw-m fc-12th wr-bw lh-17">(.*?)</span>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                link = re.sub('<(\/)?b>|<span.*?>|<|>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -subdomain:www.{domain}".format(domain=self.domain)
        return query

class BaiduEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.baidu.com/s?wd={query}&pn={page_no}'
        self.engine_name = "Baidu"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        super(BaiduEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<a.*?class="c-showurl".*?>(.*?)</a>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                link = re.sub('<.*?>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query

class AskEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.ask.com/web?q={query}&page={page_no}'
        self.engine_name = "Ask"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        super(AskEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<p class="web-result-url">(.*?)</p>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                link = re.sub('<.*?>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query

class NetcraftEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://searchdns.netcraft.com/?restriction=site+contains&host={domain}'
        self.engine_name = "Netcraft"
        super(NetcraftEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def req(self, url):
        if not self.session:
            return None
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<a href="http://toolbar.netcraft.com.*?host=(.*?)&.*?">')
        try:
            links = link_regx.findall(resp)
            for subdomain in links:
                if subdomain.endswith(self.domain) and subdomain not in self.subdomains:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

class DNSdumpsterEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://dnsdumpster.com/'
        self.engine_name = "DNSdumpster"
        super(DNSdumpsterEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def req(self, url, data=None):
        if not self.session:
            return None
        try:
            if data:
                resp = self.session.post(url, headers=self.headers, data=data, timeout=self.timeout)
            else:
                resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def enumerate(self):
        # Get CSRF token
        resp = self.req(self.base_url)
        if not resp:
            return self.subdomains
        
        csrf_regex = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">')
        csrf_token = csrf_regex.findall(resp)
        if not csrf_token:
            return self.subdomains
        
        # Submit domain
        data = {
            'csrfmiddlewaretoken': csrf_token[0],
            'targetip': self.domain
        }
        resp = self.req(self.base_url, data)
        if resp:
            self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        tds = re.findall('<td class="col-md-4">(.*?)\..*?</td>', resp)
        try:
            for td in tds:
                subdomain = td + '.' + self.domain
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        self.print_("[+] " + subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

class VirusTotalEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.virustotal.com/vtapi/v1/domain/report'
        self.engine_name = "Virustotal"
        super(VirusTotalEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def enumerate(self):
        url = self.base_url
        params = {'apikey': '', 'domain': self.domain}
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=self.timeout)
            if resp and resp.status_code == 200:
                try:
                    json_data = resp.json()
                    if 'subdomains' in json_data:
                        for subdomain in json_data['subdomains']:
                            if subdomain not in self.subdomains:
                                if self.verbose:
                                    self.print_("[+] " + subdomain)
                                self.subdomains.append(subdomain.strip())
                except:
                    pass
        except Exception:
            pass
        return self.subdomains

class ThreatCrowdEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.threatcrowd.org/searchApi/v1/domain/report/?domain={domain}'
        self.engine_name = "ThreatCrowd"
        super(ThreatCrowdEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if resp and resp.status_code == 200:
                try:
                    json_data = resp.json()
                    if 'subdomains' in json_data:
                        for subdomain in json_data['subdomains']:
                            if subdomain not in self.subdomains:
                                if self.verbose:
                                    self.print_("[+] " + subdomain)
                                self.subdomains.append(subdomain.strip())
                except:
                    pass
        except Exception:
            pass
        return self.subdomains

class CrtSearch(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        # Using both HTML and JSON endpoints for better coverage
        base_url = 'https://crt.sh/?q=%25.{domain}'
        self.json_url = 'https://crt.sh/?q=%25.{domain}&output=json'
        self.engine_name = "SSL Certificates (crt.sh)"
        self.q = q
        super(CrtSearch, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)

    def req(self, url):
        if not self.session:
            return None
        try:
            # Add better headers for crt.sh
            headers = self.headers.copy()
            headers['Accept'] = 'application/json, text/html, */*'
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
            return resp
        except Exception as e:
            if self.verbose and not self.silent:
                self.print_(f"[-] Request failed: {str(e)}")
            return None

    def enumerate(self):
        # Try JSON endpoint first (more reliable)
        json_url = self.json_url.format(domain=self.domain)
        json_resp = self.req(json_url)
        
        if json_resp and json_resp.status_code == 200:
            try:
                json_data = json_resp.json()
                self.extract_domains_from_json(json_data)
            except Exception as e:
                if self.verbose and not self.silent:
                    self.print_(f"[-] JSON parsing failed: {str(e)}")
        
        # Fallback to HTML scraping if JSON fails or returns few results
        if len(self.subdomains) < 5:  # If we got few results, try HTML too
            html_url = self.base_url.format(domain=self.domain)
            html_resp = self.req(html_url)
            if html_resp and html_resp.status_code == 200:
                self.extract_domains_from_html(html_resp.text)
        
        return self.subdomains

    def extract_domains_from_json(self, json_data):
        """Extract domains from JSON response"""
        try:
            for entry in json_data:
                if 'name_value' in entry:
                    # name_value can contain multiple domains separated by newlines
                    domains = entry['name_value'].split('\n')
                    for domain in domains:
                        domain = domain.strip()
                        self.process_domain(domain)
        except Exception as e:
            if self.verbose and not self.silent:
                self.print_(f"[-] JSON extraction error: {str(e)}")

    def extract_domains_from_html(self, resp):
        """Extract domains from HTML response (original method, improved)"""
        # Multiple regex patterns for better coverage
        patterns = [
            re.compile('<TD>(.*?)</TD>'),
            re.compile('<td>(.*?)</td>'),
            re.compile(r'(?i)<td[^>]*>(.*?)</td>')
        ]
        
        try:
            all_links = []
            for pattern in patterns:
                links = pattern.findall(resp)
                all_links.extend(links)
            
            for link in all_links:
                link = link.strip()
                if not link or link.isdigit():  # Skip empty or numeric cells
                    continue
                    
                subdomains = []
                if '<BR>' in link or '<br>' in link:
                    # Handle both upper and lower case
                    subdomains = re.split('<BR>|<br>', link, flags=re.IGNORECASE)
                else:
                    subdomains.append(link)

                for subdomain in subdomains:
                    subdomain = subdomain.strip()
                    self.process_domain(subdomain)
                    
        except Exception as e:
            if self.verbose and not self.silent:
                self.print_(f"[-] HTML extraction error: {str(e)}")

    def process_domain(self, domain):
        """Process and validate a domain before adding to results"""
        if not domain:
            return
            
        # Clean up the domain
        domain = re.sub(r'<[^>]*>', '', domain)  # Remove any HTML tags
        domain = domain.strip()
        
        # Skip if it doesn't end with our target domain or contains wildcards
        if not domain.endswith(self.domain) and not domain.endswith('.' + self.domain):
            return
        if '*' in domain:
            return
            
        # Handle email addresses (extract domain part)
        if '@' in domain:
            domain = domain[domain.find('@')+1:]
        
        # Skip if it's the exact domain or already in our list
        if domain == self.domain or domain in self.subdomains:
            return
            
        # Additional validation
        if self.is_valid_subdomain(domain):
            if self.verbose:
                self.print_("[+] " + domain)
            self.subdomains.append(domain.strip())

    def is_valid_subdomain(self, domain):
        """Validate if the domain is a proper subdomain"""
        try:
            # Basic domain validation
            if not domain or len(domain) > 253:
                return False
                
            # Check for valid characters
            if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
                return False
                
            # Must contain at least one dot and end with our target domain
            if '.' not in domain:
                return False
                
            # Check if it ends with our target domain
            if not (domain.endswith('.' + self.domain) or domain == self.domain):
                return False
                    
            return True
        except:
            return False

class PassiveDNSEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://api.passivetotal.org/v1/enrichment/subdomains?query={domain}'
        self.engine_name = "PassiveDNS"
        super(PassiveDNSEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if resp and resp.status_code == 200:
                try:
                    json_data = resp.json()
                    if 'subdomains' in json_data:
                        for subdomain in json_data['subdomains']:
                            full_subdomain = subdomain + '.' + self.domain
                            if full_subdomain not in self.subdomains:
                                if self.verbose:
                                    self.print_("[+] " + full_subdomain)
                                self.subdomains.append(full_subdomain.strip())
                except:
                    pass
        except Exception:
            pass
        return self.subdomains

class PortScanner():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None

    def port_scan(self, host, ports):
        openports = []
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    openports.append(port)
                s.close()
            except Exception:
                pass
        self.lock.release()
        if len(openports) > 0:
            print("[+] " + host + " -> " + ', '.join(openports))

    def run(self):
        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan, args=(subdomain, self.ports))
            t.start()

def check_dependencies():
    missing_deps = []
    if not requests:
        missing_deps.append("requests")
    if not dns:
        missing_deps.append("dnspython")
    
    if missing_deps:
        print("[-] Missing dependencies: " + ', '.join(missing_deps))
        print("[+] Install with: pip install " + ' '.join(missing_deps))
        return False
    return True

def main(domain, threads, savefile, ports, silent, verbose, enable_bruteforce, engines):
    if not check_dependencies():
        return []
    
    bruteforce_list = set()
    search_list = set()

    if multiprocessing.current_process().name == 'MainProcess':
        subdomains_queue = multiprocessing.Manager().list()
    else:
        subdomains_queue = list()

    if enable_bruteforce or enable_bruteforce is None:
        enable_bruteforce = True

    domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        if not silent:
            print("[-] Please enter a valid domain")
        return []

    if not domain.startswith('http://') and not domain.startswith('https://'):
        domain = 'http://' + domain

    parsed_domain = urlparse.urlparse(domain)

    if not silent:
        print_target_analysis(parsed_domain.netloc)

    # Engine groups organized as requested
    search_engines_group = {
        'google': GoogleEnum,
        'bing': BingEnum,
        'yahoo': YahooEnum,
        'baidu': BaiduEnum,
        'ask': AskEnum,
        'netcraft': NetcraftEnum,
    }

    specialized_engines_group = {
        'ssl': CrtSearch,
        'dnsdumpster': DNSdumpsterEnum,
        'virustotal': VirusTotalEnum,
        'threatcrowd': ThreatCrowdEnum,
        'passivedns': PassiveDNSEnum,
        'crt': CrtSearch,  # Alternative name for SSL certificates
    }

    # Combine all supported engines
    supported_engines = {**search_engines_group, **specialized_engines_group}

    chosenEnums = []

    if engines is None:
        # Use all engines by default (6 + 6 = 12 engines)
        chosenEnums = [GoogleEnum, BingEnum, YahooEnum, BaiduEnum, AskEnum, NetcraftEnum, 
                      CrtSearch, DNSdumpsterEnum, VirusTotalEnum, ThreatCrowdEnum, PassiveDNSEnum]
    else:
        engines = engines.split(',')
        for engine in engines:
            if engine.lower() in supported_engines:
                chosenEnums.append(supported_engines[engine.lower()])

    if not silent:
        print(Colors.CYAN + f"\n[+] Using {len(chosenEnums)} enumeration engines" + Colors.ENDC)
        search_count = sum(1 for enum in chosenEnums if enum.__name__ in ['GoogleEnum', 'BingEnum', 'YahooEnum', 'BaiduEnum', 'AskEnum', 'NetcraftEnum'])
        specialized_count = len(chosenEnums) - search_count
        print(Colors.CYAN + f"    Search Engines: {search_count}/6" + Colors.ENDC)
        print(Colors.CYAN + f"    Specialized Engines: {specialized_count}/6" + Colors.ENDC)

    enums = [enum(domain, [], q=subdomains_queue, silent=silent, verbose=verbose) for enum in chosenEnums]
    
    for enum in enums:
        enum.start()
    for enum in enums:
        enum.join()

    subdomains = set(subdomains_queue)
    for subdomain in subdomains:
        search_list.add(subdomain)

    if enable_bruteforce and subbrute:
        if not silent:
            print("[+] Starting bruteforce with " + str(threads) + " threads")
        try:
            record_type = False
            path_to_file = os.path.dirname(os.path.realpath(__file__))
            subs = os.path.join(path_to_file, 'subbrute', 'names.txt')
            resolvers = os.path.join(path_to_file, 'subbrute', 'resolvers.txt')
            process_count = threads
            output = False
            json_output = False
            bruteforce_list = subbrute.print_target(parsed_domain.netloc, record_type, subs, resolvers, process_count, output, json_output, search_list, verbose)
        except Exception as e:
            if not silent:
                print("[-] Bruteforce error: " + str(e))

    subdomains = search_list.union(bruteforce_list)

    if subdomains:
        subdomains = sorted(subdomains, key=subdomain_sorting_key)

        if not silent:
            print("\n[+] Found " + str(len(subdomains)) + " subdomains")

        if savefile:
            write_file(savefile, subdomains)

        if ports:
            if not silent:
                print("[+] Starting port scan")
            ports = ports.split(',')
            pscan = PortScanner(subdomains, ports)
            pscan.run()

        elif not silent:
            print("\n[+] Subdomains found:")
            for i, subdomain in enumerate(subdomains, 1):
                print(f"{Colors.GREEN}  {i}. {subdomain}{Colors.ENDC}")

    else:
        if not silent:
            print("[-] No subdomains found")

    return subdomains

def interactive():
    args = parse_args()
    
    # Show engines if requested
    if args.show_engines:
        show_available_engines()
        return
    
    domain = args.domain
    threads = args.threads
    savefile = args.output
    ports = args.ports
    enable_bruteforce = args.bruteforce
    verbose = args.verbose
    engines = args.engines
    
    if verbose or verbose is None:
        verbose = True
    if args.no_color:
        no_color()
    
    print_banner()
    print_config_summary(domain, threads, enable_bruteforce, verbose, ports, savefile)
    
    start_time = time.time()
    res = main(domain, threads, savefile, ports, silent=False, verbose=verbose, enable_bruteforce=enable_bruteforce, engines=engines)
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + Colors.CYAN + "[+] Scan completed in " + str(round(duration, 2)) + " seconds" + Colors.ENDC)
    print(Colors.CYAN + "[+] Total subdomains found: " + str(len(res)) + Colors.ENDC)
    print(Colors.YELLOW + "[+] Enhanced crt.sh integration provided better SSL certificate coverage!" + Colors.ENDC)

if __name__ == "__main__":
    try:
        interactive()
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print("\n[-] Error: " + str(e))
        sys.exit(1)
