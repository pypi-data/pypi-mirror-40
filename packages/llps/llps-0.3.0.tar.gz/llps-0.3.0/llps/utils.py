
from subprocess import check_output


def md5_sum(filename):
    cmd = f'openssl md5 -binary {filename} | base64'
    checksum = check_output(cmd, shell=True).decode('utf-8').strip()
    return checksum
