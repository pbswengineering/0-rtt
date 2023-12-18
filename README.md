<a href="https://www.bernardi.cloud/">
    <img src=".readme-files/logo-72.png" alt="TLS 0-RTT PoC logo" title="TLS 0-RTT PoC" align="right" height="72" />
</a>

# TLS 0-RTT PoC
> Proof of concept of a reply attack against TLS 0-RTT

[![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/github/license/pbswengineering/0-rtt.svg)](https://opensource.org/licenses/AGPL-3.0)
[![GitHub issues](https://img.shields.io/github/issues/pbswengineering/0-rtt.svg)](https://github.com/pbswengineering/0-rtt/issues)

## Table of contents

- [What is TLS 0-RTT](#what-is-tls-0-rtt)
- [Usage](#usage)
- [License](#license)
- [Credits](#credits)

## What is TLS 0-RTT

TBD

## Usage

We'll see.

`cd sslyze`

`python -m venv venv`

`. venv/bin/activate`

`pip install sslyze`

`sslyze --early-data localhost`

`sudo tcpdump "tcp port 443" -i lo -w tls.pcap`

## License

TLS 0-RTT PoC is licensed under the terms of the GNU Affero General Public License version 3.

## Credits

The Docker configuration is loosely based on [this one](https://github.com/stevenliebregt/docker-compose-lemp-stack).