---
marp: true
paginate: true
header: Network Security - M.Sc Cybersecurity - Università di Pisa
backgroundImage: url('background_internal.png')
---
<!-- _paginate: skip -->
<!-- _backgroundImage: url('background_title.png') -->
<!-- _header: . -->
<br>
<br>
<br>

<h1>Replay Attack in TLS 1.3 0-RTT Handshake: Countermeasure Techniques</h1>

<table style="width: 100%; padding: 0; margin: 0; overflow: hidden">
<tr style="background-color: rgba(0, 0, 0, 0); border: none; padding: 0; margin: 0">
<td style="width: 50%; border: none; padding: 0; margin: 0">
Network Security (933II)<br>
M.Sc. Cybersecurity<br>
Paolo Bernardi (660944)
</td>
<td style="width: 50%; border: none; padding: 0; margin: 0; overflow: hidden">
<div style="text-align: left">
<img width="400" src="unipi_logo.png">
</div>
</td>
</tr>
</table>

Version 2

---

# The Paper

  - **Conference:** 2023 IEEE 6th International Conference on Electrical, Electronics and System Engineering (ICEESE)
  - **Authors:** M. E. Abdelhafez (Malaysia), Sureswaran Ramadass (Malaysia), Mohammed S. M. Gismallab (Saudi Arabia)
  - **Goal:** review anti-replay protection techniques
  - **Keywords:** TLS 1.3, replay attack, 0-RTT, handshake

<div style="text-align: center">
<img width="300" src="ieee.jpg">
</div>

---

# Context

<table style="width: 100%; overflow: hidden">
<tr style="background-color: rgba(0, 0, 0, 0); border: none">
<td style="width: 60%; border: none">
<ul>
<li>TLS resumable connections</li>
<li>TLS 1.3 introduced <strong>0-RTT</strong> resume mode, based on a <strong>Session Ticket</strong> created during the initial full handshake encrypted with a Session Ticket Encryption Key (<strong>STEK</strong>)</li>
<li>0-RTT obtained by sending a <strong>single message</strong> that contains both the <strong>ClientHello</strong> (with a Session Ticket encrypted with a known STEK) and <strong>Application Data</strong> (also known as <strong>Early Data</strong>)</li>
</ul>
</td>
<td style="width: 40%; border: none">
<div style="text-align: left">
<img width="400" src="0-rtt_resume.png">
</div>
</td>
</tr>
</table>

---

# Attack Scenarios

<table style="width: 100%; overflow: hidden">
<tr style="background-color: rgba(0, 0, 0, 0); border: none">
<td style="width: 60%; border: none">
<ul>
<li><strong>Replay</strong> attack</li>
<li>Attacker intercepts and replays <strong>ClientHello</strong> messages with <strong>Early Data</strong></li>
<li>The replayed message is syntactically valid because the <strong>ClientHello</strong> contains a <strong>Session Ticket</strong> recognized by the server</li>
<li><strong>ALTERNATIVE SCENARIO:</strong> the attacker performs a <strong>MITM blocking server 0-RTT responses</strong> and triggering a <strong>resending</strong>
</ul>
</td>
<td style="width: 40%; border: none">
<div style="text-align: left">
<img width="400" src="0-rtt_replay.png">
</div>
</td>
</tr>
</table>

---



# Freshness check

Reject **ClientHello** messages whose **gmt_unix_time** too much in the past

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Simple implementation
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Can be inconvenient and there is an exploitable time window for attackers

# ClientHello Recording

The server keeps a list of received **ClientHello** messages and uses it to detect and discard replays 

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Can block all replay attacks
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Complex setup in distributed environments, complex synchronization

---

# Single-Use Tickets

The server **deletes** the **STEK** used to decrypt the early data after the first 0-RTT resume, making it impossible to decrypt the Session Tickets of replayed messages.

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Can block all replay attacks, no space overhead
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Complex setup in distributed environments, complex synchronization

<div style="text-align: center">
<img width="550" src="single_use_tickets_scheme.png" style="background-color: rgba(0, 0, 0, 0)">
</div>

---

# Application Profile

Each application should implement a specific **profile** that specifies under which conditions it will use 0-RTT (e.g. HTTP GET).

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Flexibility
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Not 100% safe, requires intervention at application level

# Separate API

Both client and servers use libraries that make 0-RTT usage **explicit**, rather than implicit and automatic.

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Explicit behaviour
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Requires TLS libs restructuring and programmers attention

---

# Puncture Pseudorandom Function (PPRF)

By using **PPRF** the server can decrypt 0-RTT early data only once.

**Example approach:** a server maintains a Session Ticket Encryption Key (STEK) *k* that can decrypt any session ticket. Then it uses it to decrypt a ticket *t* and it generates a STEK *k'* that can decrypt all session tickets but *t* and so on...

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Forward secrecy
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Long processing time, not practical in distributed environments


---

# Universal SSL

Introduced by **Cloudflare** in 2015 (doesn't support TLS 1.3), Universal SSL stores negotiated sessions into multiple **Memcached** instances. Each session is indexed and encrypted by **Session ID**.

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Great performance
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Memcached servers are synchronized only within each  Cloudflare PoP

<div style="text-align: center">
<img width="800" src="universal_ssl.png" style="background-color: rgba(0, 0, 0, 0)">
</div>

---

# Just-in-Time Shared Keys (JIT-SK)

Based on a **synchronized PRNG**, dynamically changes keys for each session to secure 0-RTT messages (the same key cannot be reused multiple times, so "blind replaying" is impossible).

> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>✅ Prevents replay attacks while providing forward secrecy
> <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>❌ Doesn't support distributed environments

---

# Conclusions

## 0-RTT is here to stay

The performance improvements are real (the paper states that 0-RTT resume is 44.7%  faster than 1-RTT) and the percentage of resumed TLS connections is also quite high (40% in some applications).

## 0-RTT anti-reply protection requires trade offs:

The evaluated protections introduce overheads and/or inconveniences, especially in distributed environments (e.g. CDNs), therefore 0-RTT replay protection is still an open research topic.

---
<!-- _paginate: skip -->
<!-- _backgroundImage: url('background_title.png') -->
<!-- _header: . -->

<h1 style="font-size: 300%; text-align: center">THANK YOU!</h1>

