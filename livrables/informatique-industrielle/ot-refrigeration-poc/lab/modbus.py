"""Small tested Modbus TCP subset: functions 1,2,3,4,5,6; no authentication.
Not a general production Modbus implementation. Strict MBAP framing/length checks.
"""
import socket
import socketserver
import struct
import threading
import time
from .model import Plant

class ProtocolError(Exception): pass

def recvall(sock, count):
    chunks = []
    while count:
        part = sock.recv(count)
        if not part: raise ConnectionError('connection closed')
        chunks.append(part); count -= len(part)
    return b''.join(chunks)

def handle_pdu(plant, pdu):
    if not pdu: raise ProtocolError('empty PDU')
    fn = pdu[0]
    if fn in (1, 2, 3, 4):
        if len(pdu) != 5: return bytes([fn | 128, 3])
        address, count = struct.unpack('>HH', pdu[1:])
        try: values = plant.read(fn, address, count)
        except ValueError: return bytes([fn | 128, 2])
        if fn in (3,4):
            return bytes([fn, count*2]) + struct.pack('>'+'H'*count, *values)
        bits = bytearray((count+7)//8)
        for i,v in enumerate(values):
            if v: bits[i//8] |= 1 << (i % 8)
        return bytes([fn,len(bits)]) + bytes(bits)
    if fn in (5,6):
        if len(pdu) != 5: return bytes([fn | 128, 3])
        address, value = struct.unpack('>HH', pdu[1:])
        try:
            if fn == 5:
                if value not in (0,0xff00): raise ValueError('bad coil value')
                plant.write_coil(address, value == 0xff00)
            else: plant.write_register(address, value)
        except ValueError: return bytes([fn | 128, 3])
        return pdu
    return bytes([fn | 128, 1])

class TCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    def __init__(self, address, plant):
        self.plant = plant
        super().__init__(address, Handler)

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = self.request
        sock.settimeout(5)
        while True:
            try:
                header = recvall(sock, 7)
                tid, protocol, length, uid = struct.unpack('>HHHB', header)
                if protocol != 0 or not (2 <= length <= 254): return
                pdu = recvall(sock, length-1)
                response = handle_pdu(self.server.plant, pdu)
                sock.sendall(struct.pack('>HHHB', tid, 0, len(response)+1, uid) + response)
            except (ConnectionError, OSError, TimeoutError): return

def simulation_loop(plant, stop, period=0.1):
    while not stop.wait(period): plant.advance(period)

def start_lab(host='127.0.0.1', port=15020, period=0.1):
    plant = Plant(); stop = threading.Event()
    server = TCPServer((host,port), plant)
    controller_thread = threading.Thread(target=simulation_loop, args=(plant,stop,period), daemon=True)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    controller_thread.start(); server_thread.start()
    return plant,server,stop

class Client:
    def __init__(self,host='127.0.0.1',port=15020,timeout=3): self.host,self.port,self.timeout=host,port,timeout
    def request(self,fn,address,value):
        pdu = struct.pack('>BHH',fn,address,value)
        req = struct.pack('>HHHB',1,0,len(pdu)+1,1)+pdu
        with socket.create_connection((self.host,self.port),self.timeout) as s:
            s.settimeout(self.timeout)
            s.sendall(req)
            h=recvall(s,7)
            tid,proto,length,uid=struct.unpack('>HHHB',h)
            if tid!=1 or proto!=0 or length<2 or length>254: raise ProtocolError('bad MBAP response')
            response=recvall(s,length-1)
        if response[0] & 128: raise ProtocolError(f'Modbus exception code {response[1]}')
        if response[0]!=fn: raise ProtocolError('wrong function code')
        if fn in (3,4):
            if response[1]!=2*value or len(response)!=2+2*value: raise ProtocolError('invalid register payload')
            return list(struct.unpack('>'+'H'*value,response[2:]))
        if fn in (1,2):
            return [(response[2+(i//8)]>>(i%8)) & 1 for i in range(value)]
        if response!=pdu: raise ProtocolError('write echo mismatch')
        return True
