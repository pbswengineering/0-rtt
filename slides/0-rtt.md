---
marp: true
paginate: true
header: Network Security - M.Sc Cybersecurity - Università di Pisa
backgroundImage: url('background_internal.png')
---
<!-- _paginate: skip -->
<!-- _backgroundImage: url('background_title.png') -->
<br>

# Replay Attack in TLS 1.3 0-RTT Handshake: Countermeasure Techniques

<table style="width: 100%">
<tr style="background-color: rgba(0, 0, 0, 0); border: none">
<td style="width: 50%; border: none">
Network Security (933II)<br>
M.Sc. Cybersecurity<br>
Paolo Bernardi (660944)
</td>
<td style="width: 50%; border: none">
<div style="text-align: left">
<img width="400" src="unipi.png">
</div>
</td>
</tr>
</table>

---

# 1. Paper

  - **Conference:** 2023 IEEE 6th International Conference on Electrical, Electronics and System Engineering (ICEESE)
  - **Authors:** M.E Abdelhafez (Malaysia), Sureswaran Ramadass (Malaysia), Mohammed S. M. Gismallab (Saudi Arabia)
  - **Goal:** review anti-replay protection techniques
  - **Keywords:** TLS 1.3, replay attack, 0-RTT, handshake

---

# 2. Context

<table style="width: 100%">
<tr style="background-color: rgba(0, 0, 0, 0); border: none">
<td style="width: 60%; border: none">
<ul>
<li>TLS resumable connections</li>
<li>TLS 1.3 introduced <strong>0-RTT</strong> resume mode, based on a <strong>Session-Ticket key</strong> created during the initial full handshake</li>
<li>0-RTT obtained by sending a <strong>single message</strong> that contains both the <strong>ClientHello</strong> (with a known Session-Ticket key) and <strong>Application Data</strong> (also known as <strong>Early Data</strong>)</li>
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

# 3. Attack Scenarios

<table style="width: 100%">
<tr style="background-color: rgba(0, 0, 0, 0); border: none">
<td style="width: 60%; border: none">
<ul>
<li><strong>Replay</strong> attack</li>
<li>Attacker intercepts and replays <strong>ClientHello</strong> messages with <strong>Early Data</strong></li>
<li>The replayed message is valid because the <strong>ClientHello</strong> contains a <strong>Session-Ticket key</strong> recognized by the server</li>
<li><strong>ALTERNATIVE SCENARIO:</strong> the attacker performs a <strong>MITM</strong> and makes the client <strong>to believe that the 0-RTT message wasn't received</strong>, triggering a resending
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

# 4a. Freshness check

Reject **ClientHello** messages whose **gmt_unix_time** is outside a predetermined time frame

# 4b. Client-Hello Recording

The server keeps a list of received **ClientHello** messages and uses it to detect and discard replays (**ACHTUNG: complex setup in distributed scenarios**)

---

# 5a. Single-Use Tickets

# 5b. Application Profile

---

# 6. Separate API

---

# 7. Puncture Pseudorandom Function (PPRF)

---

# 8. Universal SSL

---

# 9. Just-in-Time Shared Keys (JIT-SK)

---

# 10. Conclusions

  - **0-RTT is here to stay**: the performance improvements are real (the paper stats that 0-RTT resume is 44.7% than 1-RTT) and the percentage of resumed TLS connections is also quite high (40% ins some applications)
  - **0-RTT anti-reply protection requires trade offs:** the evaluated protections introduce overheads and/or inconveniences;
  - **JIT-SK** is the most promising protection for high traffic networks but it might not be interoperable with existing TLS 1.3 systems and anti-reply me
