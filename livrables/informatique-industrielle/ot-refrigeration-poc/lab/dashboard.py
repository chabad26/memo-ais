"""Read-only HTTP dashboard; independent from FUXA."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .modbus import Client
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Cold room OT lab</title><style>body{font:18px sans-serif;max-width:650px;margin:40px auto}div{padding:12px;border-bottom:1px solid #bbb}.alarm{color:crimson}</style></head><body><h1>Cold room — simulated HMI</h1><p>Read-only Modbus values. Use the CLI for writes.</p><div id="status">Loading…</div><script>async function update(){try{const r=await fetch('/api');if(!r.ok)throw Error('offline');const x=await r.json();document.getElementById('status').innerHTML='<div>Temperature: '+x.temperature+' °C</div><div>Setpoint: '+x.setpoint+' °C</div><div>Compressor: '+(x.compressor?'ON':'OFF')+'</div><div>Door: '+(x.door?'OPEN':'CLOSED')+'</div><div class="'+(x.alarm?'alarm':'')+'">Alarm: '+(x.alarm?'HIGH TEMPERATURE':'none')+'</div>'}catch(e){document.getElementById('status').textContent='PLC unavailable'}}update();setInterval(update,1000)</script></body></html>'''
def serve(host,port,plc_host,plc_port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/': data=HTML.encode();ct='text/html; charset=utf-8'
            elif self.path=='/api':
                try:
                    c=Client(plc_host,plc_port);i=c.request(4,0,4);h=c.request(3,0,1);b=c.request(1,0,1)
                    data=json.dumps(dict(temperature=i[0]/10,setpoint=h[0]/10,compressor=bool(i[1]),alarm=bool(i[2]),door=bool(b[0]))).encode();ct='application/json'
                except Exception:
                    self.send_error(503,'PLC unavailable');return
            else: self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',ct);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    ThreadingHTTPServer((host,port),Handler).serve_forever()
def main():
    p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=18080);p.add_argument('--plc-host',default='127.0.0.1');p.add_argument('--plc-port',type=int,default=15020)
    a=p.parse_args();serve(a.host,a.port,a.plc_host,a.plc_port)
if __name__=='__main__':main()
