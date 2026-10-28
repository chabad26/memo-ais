"""Educational Modbus TCP proxy. Allows read functions 1–4; blocks writes 5/6.
Runs at the IT/OT boundary. Not a firewall, DPI, or production security product.
"""
import argparse
import socket
import socketserver
import struct
from .modbus import recvall

class Gateway(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
    daemon_threads=True
    def __init__(self,addr,upstream):self.upstream=upstream;super().__init__(addr,Handler)
class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(3)
        while True:
            try:
                header=recvall(self.request,7)
                tid,proto,length,uid=struct.unpack('>HHHB',header)
                if proto!=0 or not (2<=length<=254): return
                pdu=recvall(self.request,length-1)
                if pdu[0] not in (1,2,3,4):
                    reply=bytes([pdu[0]|128,1])
                else:
                    with socket.create_connection(self.server.upstream,timeout=3) as s:
                        s.settimeout(3);s.sendall(header+pdu)
                        h=recvall(s,7);t,pr,ln,u=struct.unpack('>HHHB',h)
                        if t!=tid or pr!=0 or u!=uid or not(2<=ln<=254):return
                        reply=recvall(s,ln-1)
                self.request.sendall(struct.pack('>HHHB',tid,0,len(reply)+1,uid)+reply)
            except (ConnectionError,OSError,TimeoutError):return

def main():
    p=argparse.ArgumentParser(description='Read-only Modbus gateway for demo')
    p.add_argument('--listen-host',default='127.0.0.1');p.add_argument('--listen-port',type=int,default=15021)
    p.add_argument('--upstream-host',default='127.0.0.1');p.add_argument('--upstream-port',type=int,default=15020)
    a=p.parse_args();g=Gateway((a.listen_host,a.listen_port),(a.upstream_host,a.upstream_port))
    print(f'Read-only proxy listening on {g.server_address}',flush=True)
    try:g.serve_forever()
    except KeyboardInterrupt:pass
    finally:g.server_close()
if __name__=='__main__':main()
