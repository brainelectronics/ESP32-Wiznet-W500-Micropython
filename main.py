#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
ESP32 with WIZNET5500 example usage

MicroPython WIZNET5K documentation, see
https://docs.micropython.org/en/latest/library/network.WIZNET5K.html

Picoweb example
https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/example_webapp.py
"""

from machine import Pin, SPI
from struct import unpack
from time import sleep, localtime, ticks_diff, ticks_ms
from wiznet5k import WIZNET5K
import wiznet5k_socket as socket


spi = SPI(1)
cs = Pin(15, Pin.OUT)
# defining rst pin as output, resets the W5500 for ever
# rst = Pin(19, Pin.OUT)
# rst.on()  # stop resetting W5500
# sleep(1)     # wait until W5500 "booted"
nic = WIZNET5K(spi_bus=spi, cs=cs)  # debug=True
print('NIC created: {}'.format(nic))

connection_timeout = 10 * 1000    # connection timeout in milliseconds
start_ms = ticks_ms()
while (ticks_diff(ticks_ms(), start_ms) <= connection_timeout):
    print('Waiting for WIZNET connection...')
    if nic.link_status:
        print('Connection to network established')
        break
    sleep(1)

# print general details
print('Chip Version: {}'.format(nic.chip))
print('MAC Address: {}'.format([hex(i) for i in nic.mac_address]))
print('IP address: {}'.format(nic.pretty_ip(nic.ip_address)))
print('Max number of sockets: {}'.format(nic.max_sockets))
print('IP lookup time.google.com: {}'.
      format(nic.pretty_ip(nic.get_host_by_name('time.google.com'))))

# create socket connection to Google time server
addr = socket.getaddrinfo('time.google.com', 123)[0][-1]
data = b'\x1b' + 47 * b'\x00'
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(1)
client.sendto(data, addr)
recv_data, address = client.recvfrom(1024)
print('Received data: {}'.format(recv_data))

t = unpack('!12I', recv_data)[10]
print('Extracted time: {}'.format(t))
t = t - 3155673600

print('Local time: {}'.format(localtime(t)))

"""
# Picoweb used Asyncio, which is not working with this WIZNET5K code
# https://github.com/micropython/micropython/issues/8938

import picoweb
import ulogging as logging
import ure as re


def index(req, resp):
    # You can construct an HTTP response completely yourself, having
    # a full control of headers sent...
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/html\r\n")
    yield from resp.awrite("\r\n")
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.<br/>")
    yield from resp.awrite("Or my <a href='file'>source</a>.")


def squares(req, resp):
    # Or can use a convenience function start_response() (see its source for
    # extra params it takes).
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req,))


def hello(req, resp):
    yield from picoweb.start_response(resp)
    # Here's how you extract matched groups from a regex URI match
    yield from resp.awrite("Hello " + req.url_match.group(1))


ROUTES = [
    # You can specify exact URI string matches...
    ("/", index),
    ("/squares", squares),
    ("/file", lambda req, resp: (yield from app.sendfile(resp,
                                                         "example_webapp.py"))),
    # ... or match using a regex, the match result available as req.url_match
    # for match group extraction in your view.
    (re.compile("^/iam/(.+)"), hello),
]


app = picoweb.WebApp(__name__, ROUTES)

# debug values:
# -1 disable all logging
# 0 (False) normal logging: requests and errors
# 1 (True) debug logging
# 2 extra debug logging
app.run(host=nic.pretty_ip(ip=nic.ip_address), port=80, debug=2)
"""

print('Returning to REPL')
