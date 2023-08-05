# Copyright © 2018 Absolute Performance, Inc
# Written by Taylor C. Richberger <taywee@gmx.com>

import locale
import argparse
import json
import re
import subprocess
from collections import namedtuple

from strictyaml import load
import paramiko

from . import __version__, __description__
from .config import schema

# Fix broken iperf3 behavior: https://github.com/esnet/iperf/issues/826
NANREPLACE = re.compile(r'":\s*-?nan,$', re.IGNORECASE | re.MULTILINE)

class Datapoint:
    def __init__(self, dkey, metric=0, status=0, message=''):
        self.dkey = dkey
        self.metric = metric
        self.status = status
        self.message = message

    def __str__(self):
        return '\t'.join((str(self.dkey), str(self.metric), str(self.status), str(self.message)))

# Used to present an argparse-compatible API for StrictYaml 
Config = namedtuple('Config', ['clientflags', 'serverflags', 'host', 'username', 'password', 'keyfilename', 'port', 'dkeyprefix'])

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-V', '--version', action='version', version=str(__version__))
    parser.add_argument('-c', '--config', help='Take a config file instead of command line parameters')
    parser.add_argument('-d', '--dkeyprefix', help='The datapoint dkey prefix')
    parser.add_argument('-f', '--clientflags', help='Pass additional flags to the client invocation (in addition to the usual -Js1)')
    parser.add_argument('-F', '--serverflags', help='Pass additional flags to the server invocation (in addition to the usual -J1)')
    parser.add_argument('-H', '--host', help='The remote host to use')
    parser.add_argument('-u', '--username', help='The ssh username to use')
    parser.add_argument('-p', '--password', help='The ssh password to use')
    parser.add_argument('-k', '--keyfilename', help='The ssh key filename to use')
    parser.add_argument('-P', '--port', type=int, help='The ssh port to use, otherwise let iperf3 decide', default=-1)
    args = parser.parse_args()

    # Set up config
    if args.config:
        with open(args.config, 'r') as file:
            yaml = load(file.read(), schema)
        config = Config(
            clientflags=yaml.get('clientflags'),
            serverflags=yaml.get('serverflags'),
            host=yaml.get('host'),
            username=yaml.get('username'),
            password=yaml.get('password'),
            keyfilename=yaml.get('keyfilename'),
            port=yaml.get('port'),
            dkeyprefix=yaml.get('dkeyprefix'),
        )
    else:
        config = args

    # Run the server on the remote side and connect to it from this side, collecting the data.
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if config.password is None:
            ssh.connect(str(config.host), username=str(config.username), key_filename=str(config.keyfilename))
        else:
            ssh.connect(str(config.host), username=str(config.username), password=str(config.password))

        command = ['iperf3', '-Js1']

        if config.port > 0:
            command += ['-p', str(config.port)]
        if config.serverflags is not None:
            command.append(str(config.serverflags))

        # Start up server side
        stdin, stdout, stderr = ssh.exec_command(' '.join(command))

        command = ['iperf3', '-Jc', str(config.host)]

        if config.port > 0:
            command += ['-p', str(config.port)]
        if config.clientflags is not None:
            command.append(str(config.clientflags))

        # Start up client side
        response = subprocess.check_output(command, timeout=30)

        # Fix broken iperf3 behavior: https://github.com/esnet/iperf/issues/826
        local = json.loads(NANREPLACE.sub('": null,', str(response, 'utf-8')))
        remote = json.loads(NANREPLACE.sub('": null,', str(stdout.read(), 'utf-8')))

    prefix = str(config.dkeyprefix)
    # Output local datapoints
    for category, data in local['end'].items():
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    print(Datapoint(dkey='|'.join((prefix, 'local', category, key)), metric=value))

    # Output remote datapoints
    for category, data in remote['end'].items():
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    print(Datapoint(dkey='|'.join((prefix, 'remote', category, key)), metric=value))

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    main()
