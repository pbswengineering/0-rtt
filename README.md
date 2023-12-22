<a href="https://www.bernardi.cloud/">
    <img src=".readme-files/logo-72.png" alt="TLS 0-RTT PoC logo" title="TLS 0-RTT PoC" align="right" height="72" />
</a>

# TLS 0-RTT PoC
> Proof of concept of a reply attack against TLS 0-RTT

[![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![GitHub issues](https://img.shields.io/github/issues/pbswengineering/0-rtt.svg)](https://github.com/pbswengineering/0-rtt/issues)

## Table of contents

- [What is TLS 0-RTT](#what-is-tls-0-rtt)
- [Usage](#usage)
- [License](#license)
- [Credits](#credits)

## What is TLS 0-RTT

[TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) comprises a 0-RTT mode that allows clients to send application data within a `ClientHello` message right after a fresh SSL session with a full 1-RTT handshake has been established. Such application data is called *early data*.

The 0-RTT mode of operation is subject to [reply attacks](https://www.rfc-editor.org/rfc/rfc8470). Over time several mitigations were put in place within TLS libraries, however the problem still remains.

## Usage

In order to witness a 0-RTT reply attack at work the containers expose a mock "banking application":
  - `https://localhost:443`: unprotected NGINX
  - `https://localhost:444`: protected NGINX

First you should start the docker containers with two instances of NGINX:
  - on port 443 you'll find a version of NGINX compiled with the `SSL_OP_NO_ANTI_REPLAY`, to disable OpenSSL anti-reply protections;
  - on port 444 you'll find a vanilla NGINX with the anti-replay protection.

The containers can be started with `docker-compose` but there is a convenient script:

    $ scripts/containers.sh

After starting the containers can witness 0-RTT reply attacks by using the `tls_playback.py` tool.

Firstly you should create and activate a suitable Python virtual environment:

    $ cd scripts
    $ pip install -r requirements.txt
    $ . venv/bin/activate

Secondly you can prepare the replay attack with one of the following scripts that wrap `tls_playback.py`:

  1. `scripts/replay.sh`: performs a "classic" replay attack against the NGINX without protections;
  2. `scripts/replay-prot.sh`: performs a "classic" replay attack against the protected NGINX;
  3. `scripts/replay-retry.sh`: forces the client to retry the request while forwarding it to the server.

Finally you can start the command line client, which will connect to `localhost:4443` (the port open by the replay tool) and perform a money transfer (e.g. sending 50 to the user "test"), then you can open your web browser, refresh the banking application and verify the balance and the transfer operations.

## License

TLS 0-RTT PoC is licensed under the terms of the 2-clauses BSD license.

## Credits

  - The Docker configuration is (very loosely) based on [this one](https://github.com/stevenliebregt/docker-compose-lemp-stack)
  - The `tls_playback.py` tool was developed by [Alfonso García Alguacil and Alejo Murillo Moya](https://labs.portcullis.co.uk/presentations/playback-a-tls-1-3-story-2/)
  - The command line banking client is based on the [sslyze](https://github.com/nabla-c0d3/sslyze) `early_data_plugin.py`