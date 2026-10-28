import sys
import argparse
from .modbus import Client
from lab.modbus import ProtocolError

def main():
    p=argparse.ArgumentParser(description='Modbus client: reads, writes and demo faults')
    p.add_argument('operation',choices=['status','setpoint','door','sensor-fault','auto'])
    p.add_argument('value',nargs='?')
    p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=15020)
    args=p.parse_args(); c=Client(args.host,args.port)
    if args.operation=='status':
        hr=c.request(3,0,3); ir=c.request(4,0,4); coils=c.request(1,0,2)
        print(f'temp={ir[0]/10:.1f} C; setpoint={hr[0]/10:.1f} C; compressor={ir[1]}; alarm={ir[2]}; door={coils[0]}; sensor_fault={ir[3]}; auto={hr[2]}')
    else:
        if args.value is None: p.error('value required')
        if args.operation=='setpoint': c.request(6,0,round(float(args.value)*10))
        elif args.operation=='door': c.request(5,0,0xff00 if int(args.value) else 0)
        elif args.operation=='sensor-fault': c.request(5,1,0xff00 if int(args.value) else 0)
        else: c.request(6,2,int(args.value))
        print('write accepted')

if __name__ == '__main__':
    try:
        main()
    except ProtocolError as e:
        print(f"Modbus operation failed: {e}", file=sys.stderr)
        sys.exit(1)
