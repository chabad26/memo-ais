import argparse
import time
from .modbus import start_lab

def main():
    p=argparse.ArgumentParser(description='Simulated refrigeration PLC (Modbus TCP subset)')
    p.add_argument('--host',default='127.0.0.1'); p.add_argument('--port',type=int,default=15020)
    args=p.parse_args()
    plant,server,stop=start_lab(args.host,args.port)
    print(f'Listening on {args.host}:{server.server_address[1]} (Modbus TCP), Ctrl-C to stop',flush=True)
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: pass
    finally:
        stop.set();server.shutdown();server.server_close()
if __name__=='__main__': main()
