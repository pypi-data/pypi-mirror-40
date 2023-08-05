#!/usr/bin/env python3
# Copyright (c) 2018 EPAM Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import logging
from OpenSSL import crypto


logger = logging.getLogger(__name__)


_OUTPUT_DIR = "secure_dir"
_PUBLIC_NAME = "public_key.pem"
_PRIVATE_NAME = "private_key.pem"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate public and private keys",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-o", "--output-dir", dest="output_dir", default=_OUTPUT_DIR,
                        help="Output directory for saving keys.")
    parser.add_argument("--pub-key-name", dest="pub_key_name", default=_PUBLIC_NAME,
                        help="File name for public key.")
    parser.add_argument("--private-key-name", dest="private_key_name", default=_PRIVATE_NAME,
                        help="File name for private key")

    return parser.parse_args()


def save_keys(public_key, private_key, output=_OUTPUT_DIR, public_file=_PUBLIC_NAME, private_file=_PRIVATE_NAME):
    """Saves a key pair content in files."""
    if not os.path.exists(output):
        os.makedirs(output)

    logger.debug("Saving the keys in %s", output)

    pub_file = os.path.join(output, public_file)
    with open(pub_file, 'wb') as cert:
        cert.write(public_key)

    key_file = os.path.join(output, private_file)
    with open(key_file, 'wb') as key:
        key.write(private_key)


def generate_pairs(crypto_type=crypto.TYPE_RSA, bits=2048):
    """Generates keys (public/private) based on type and bits."""
    key = crypto.PKey()
    key.generate_key(crypto_type, bits)

    public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
    private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)

    return public_key, private_key


def main():
    args = parse_args()
    public_key, private_key = generate_pairs()
    save_keys(public_key, private_key,
              output=args.output_dir, public_file=args.pub_key_name, private_file=args.private_key_name)
    print(public_key.decode())


if __name__ == '__main__':
    main()
