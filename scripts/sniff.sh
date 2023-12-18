#!/usr/bin/env bash
tcpdump "tcp port 443" -i lo -w tls.pcap