#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Thomas Bechtold <thomasbechtold@jpberlin.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import shutil
import subprocess
import tempfile
import uuid


USER_DATA = """#cloud-config
debug: True
ssh_authorized_keys:
  - {}
"""

META_DATA = """instance-id: {}
local-hostname: cloudy
"""

ISO_CMDS = ['mkisofs', 'genisoimage']

def _get_iso_image_cmd():
    """get the full path to mkisofs or genisoimage or None
    if both are not available"""
    for prog in ISO_CMDS:
        p = shutil.which(prog)
        if p:
            return p
    return None


def create(args):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'user-data'), 'w') as ud:
            ud.write(USER_DATA.format(args.ssh_pub_key.read()))
        with open(os.path.join(tempdir, 'meta-data'), 'w') as md:
            md.write(META_DATA.format(uuid.uuid4()))
        prog = _get_iso_image_cmd()
        if not prog:
            raise Exception('None of the commands {} found'.format(ISO_CMDS))
        args = [prog,
                '-output', args.outfile,
                '-volid', 'cidata',
                '-joliet', '-rock',
                tempdir]
        subprocess.check_call(args, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)


def parse_args():
    parser = argparse.ArgumentParser(
        description='cloud-init seed image creation')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create
    parser_create = subparsers.add_parser(
        'create', help='Create an cloud-init compatible seed image')
    parser_create.add_argument('--outfile', type=str, default='seed.img',
                              help='Path to the output seed file. Defaults'
                              ' to %(default)s')
    parser_create.add_argument('--ssh-pub-key',
                               type=argparse.FileType('r'),
                               default=os.path.expanduser('~/.ssh/id_rsa.pub'),
                               help='Path to the ssh public key file. '
                               'Defaults to "%(default)s"')
    parser_create.set_defaults(func=create)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
