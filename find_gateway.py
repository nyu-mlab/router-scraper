import platform
import subprocess
import re

def find_gateway():
    '''Get Default Wifi Gateway'''

    checkSystem = platform.system()

    if checkSystem == 'Linux' or checkSystem == 'Darwin':
        cmd = 'ip r | grep default'

    elif checkSystem == 'Windows':
        cmd = 'ipconfig | findstr "Default Gateway"'

    # Execute the command and store the result as a string object   
    results = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout
    # IPv4
    urls = re.findall( r'[0-9]+(?:\.[0-9]+){3}', results)
    ipv4 = True
    # IPv6
    if not urls:
        urls = re.findall( r'^([0-9a-f]{0,4}:){2,7}(:|[0-9a-f]{1,4})', results)
        ipv4 = False

    # TODO: May have multiple default gateways
    if ipv4: url = urls[-1]
    else: url = '[' + urls[-1] + ']'

    return "http://" + url