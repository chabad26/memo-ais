import json
import socket
import struct
import time
import unittest
from urllib.request import urlopen
from threading import Thread
from http.server import ThreadingHTTPServer
from lab.model import Plant
from lab.modbus import Client,ProtocolError,start_lab,handle_pdu
from lab.dashboard import serve

class PlantTests(unittest.TestCase):
    def test_compressor_cools(self):
        p=Plant(temp=10); p.advance(10)
        self.assertTrue(p.compressor);self.assertLess(p.temp,10)
    def test_door_accelerates_heat(self):
        a=Plant(temp=4,compressor=False,automatic=False);b=Plant(temp=4,compressor=False,automatic=False,door_open=True)
        a.advance(10); b.advance(10);self.assertGreater(b.temp,a.temp)
    def test_failsafe(self):
        p=Plant(temp=12,sensor_fault=True);p.advance(1);self.assertFalse(p.compressor)
    def test_alarm_delay(self):
        p=Plant(temp=12,automatic=False)
        p.advance(9);self.assertFalse(p.alarm)
        p.advance(2);self.assertTrue(p.alarm)
    def test_invalid_register(self):
        p=Plant();self.assertEqual(handle_pdu(p,bytes([3,0,0,0,4])),bytes([0x83,2]))
    def test_invalid_setpoint(self):
        p=Plant();self.assertEqual(handle_pdu(p,bytes([6,0,0,0xff,0xff])),bytes([0x86,3]))

class NetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.plant,cls.server,cls.stop=start_lab(port=0);cls.port=cls.server.server_address[1]
    @classmethod
    def tearDownClass(cls):cls.stop.set();cls.server.shutdown();cls.server.server_close()
    def test_modbus_roundtrip(self):
        c=Client(port=self.port)
        self.assertEqual(c.request(3,0,1),[40]);self.assertTrue(c.request(6,0,500))
        self.assertEqual(c.request(3,0,1),[500])
        self.assertTrue(c.request(6,0,40))
        self.assertEqual(c.request(1,0,2),[0,0])
        self.assertTrue(c.request(5,0,0xff00));self.assertEqual(c.request(1,0,1),[1]);c.request(5,0,0)
    def test_exception(self):
        with self.assertRaises(ProtocolError):Client(port=self.port).request(3,99,1)
    def test_real_tcp_mbap(self):
        with socket.create_connection(('127.0.0.1',self.port)) as s:
            s.sendall(bytes.fromhex('123400000006010300000001'))
            response=s.recv(1024)
        self.assertEqual(response[:7],bytes.fromhex('12340000000501'))
        self.assertEqual(response[7:9],bytes([3,2]))
    def test_dangerous_setpoint(self):
        c=Client(port=self.port);c.request(6,0,500)
        self.assertEqual(self.plant.snapshot()['setpoint'],50)
        c.request(6,0,40)

if __name__=='__main__':unittest.main()

class GatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lab.gateway import Gateway
        cls.plant,cls.plc,cls.stop=start_lab(port=0)
        cls.gw=Gateway(('127.0.0.1',0),('127.0.0.1',cls.plc.server_address[1]))
        cls.thread=Thread(target=cls.gw.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.gw.shutdown();cls.gw.server_close();cls.stop.set();cls.plc.shutdown();cls.plc.server_close()
    def test_allow_reads_block_writes(self):
        c=Client(port=self.gw.server_address[1]); self.assertEqual(c.request(3,0,1),[40])
        with self.assertRaises(ProtocolError):c.request(6,0,500)
        self.assertEqual(Client(port=self.plc.server_address[1]).request(3,0,1),[40])
