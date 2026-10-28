"""Black-box process tests: launch actual CLI services and request dashboard over HTTP."""
import json
import os
import socket
import subprocess
import sys
import time
import unittest
from urllib.request import urlopen
ROOT=os.path.dirname(os.path.dirname(__file__))
def free_port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def wait_for_port(port,deadline=5):
    start=time.monotonic()
    while time.monotonic()-start<deadline:
        try:
            with socket.create_connection(('127.0.0.1',port),.2):return
        except OSError:time.sleep(.05)
    raise AssertionError(f'service on port {port} did not start')
class CLITests(unittest.TestCase):
    def test_server_client_dashboard_and_gateway(self):
        plc_port,gw_port,http_port=free_port(),free_port(),free_port()
        procs=[]
        def launch(*args):
            proc=subprocess.Popen([sys.executable,'-m',*args],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            procs.append(proc)
            return proc
        try:
            launch('lab.server','--port',str(plc_port));wait_for_port(plc_port)
            launch('lab.dashboard','--port',str(http_port),'--plc-port',str(plc_port));wait_for_port(http_port)
            launch('lab.gateway','--listen-port',str(gw_port),'--upstream-port',str(plc_port));wait_for_port(gw_port)
            def cli(*args):
                return subprocess.check_output([sys.executable,'-m','lab.client',*args,'--port',str(plc_port)],cwd=ROOT,text=True)
            self.assertIn('setpoint=4.0 C',cli('status'))
            self.assertIn('accepted',cli('setpoint','50'))
            with urlopen(f'http://127.0.0.1:{http_port}/api',timeout=3) as response:
                self.assertEqual(json.loads(response.read())['setpoint'],50)
            with urlopen(f'http://127.0.0.1:{http_port}/',timeout=3) as response:
                self.assertIn(b'Cold room',response.read())
            from lab.modbus import Client,ProtocolError
            self.assertEqual(Client(port=gw_port).request(3,0,1),[500])
            with self.assertRaises(ProtocolError):Client(port=gw_port).request(6,0,40)
        finally:
            for p in procs:p.terminate()
            for p in procs:
                try:p.wait(timeout=3)
                except subprocess.TimeoutExpired:p.kill();p.wait()
if __name__=='__main__':unittest.main()
