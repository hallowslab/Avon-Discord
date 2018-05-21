import platform
import subprocess

current_os = platform.system()


def ping(host):
    if current_os.lower() == "windows":
        return subprocess.call("ping" + " -n 1 " + host) == 0
    else:
        return subprocess.call(["ping", "-c 1", host]) == 0
