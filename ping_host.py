from platform  import system as system_name
import subprocess

def ping(host):
    param = ' -n 1 ' if system_name().lower()=='windows' else ' -c 1 '
    command = 'ping' + param + host
    return subprocess.call(["ping", "-c 1", host]) == 0

ping("google.com")
