import os.path
import socket
from concurrent.futures import ThreadPoolExecutor

import paramiko
from iprange import iprange
from paramiko import SSHException

RSA_KEY = "~/Downloads/id_rsa"
SSH_USERNAME = ""
USERNAME = ""
PASSWORD = ""
TIMEOUT = 5


def check_connect_with_key(hostname: str) -> bool:
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=hostname,
            username=SSH_USERNAME,
            pkey=paramiko.RSAKey.from_private_key_file(os.path.expanduser(RSA_KEY)),
            timeout=TIMEOUT,
        )
        print(f"Connection by Key Succeeded! {hostname=}")
    except (socket.error, SSHException):
        return False
    else:
        return True
    finally:
        client.close()


def check_connect_with_pass(hostname: str) -> bool:
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=hostname, username=USERNAME, password=PASSWORD, timeout=TIMEOUT
        )
        print(f"Connection by Credentials Succeeded! {hostname=}")
    except (socket.error, SSHException):
        return False
    else:
        return True
    finally:
        client.close()

def task(hostname: str) -> None:
    if not any((check_connect_with_pass(hostname), check_connect_with_key(hostname))):
        print("Neither RSA key nor Credentials worked for host", hostname)

if __name__ == "__main__":
    with ThreadPoolExecutor(10) as executor:
        list(executor.map(task, iprange("INSERT_IP_RANGE_HERE")))