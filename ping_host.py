from platform  import system as system_name
from subprocess import call as system_call

def ping(host):
    param = ' -n 1' if system_name().lower()=='windows' else ' -c 1'
    command = 'ping' + param + " " + host
    return system_call(command) == 0
