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
    
    url = ''
    # IPv4
    # TODO: May have multiple default gateways
    urls = re.findall( r'[0-9]+(?:\.[0-9]+){3}', results)
    if urls:
        url = urls[-1]
    else:
        # IPv6
        # This regular expression does not work on At&T router
        # urls = re.findall( r'^([0-9a-f]{0,4}:){2,7}(:|[0-9a-f]{1,4})', results)
        url = results[results.lower().find('fe80'):results.lower().find('%')]
        url = '[' + url + ']'

    return "http://" + url