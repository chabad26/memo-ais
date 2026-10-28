"""Deterministic process and PLC control model (no external dependencies)."""
from dataclasses import dataclass, field
from threading import RLock
import time

@dataclass
class Plant:
    temp: float = 5.0
    ambient: float = 22.0
    setpoint: float = 4.0
    door_open: bool = False
    sensor_fault: bool = False
    compressor: bool = False
    alarm: bool = False
    automatic: bool = True
    alarm_seconds: float = 0.0
    lock: RLock = field(default_factory=RLock, repr=False)
    # Holding registers: 0=setpoint C*10; 1=limit C*10; 2=mode 1=auto
    # Input registers: 0=temperature C*10; 1=compressor; 2=alarm; 3=sensor fault
    # Coils: 0=door open; 1=sensor fault (fault injection)
    # Discrete inputs: 0=compressor; 1=high-temp alarm
    def advance(self, dt: float):
        with self.lock:
            if self.sensor_fault:
                self.compressor = False  # training-only fail-safe assumption
            elif self.automatic:
                if self.temp >= self.setpoint + 0.5:
                    self.compressor = True
                elif self.temp <= self.setpoint - 0.5:
                    self.compressor = False
            heat = 0.0007 * (self.ambient - self.temp) * (2.0 if self.door_open else 1.0)
            cool = 0.040 if self.compressor else 0.0
            self.temp += (heat - cool) * dt
            self.temp = max(-10.0, min(60.0, self.temp))
            self.alarm_seconds = (self.alarm_seconds + dt) if self.temp > 8 else 0.0
            self.alarm = self.alarm_seconds >= 10.0
    def snapshot(self):
        with self.lock:
            return dict(temp=round(self.temp, 2), setpoint=self.setpoint,
                        compressor=self.compressor, alarm=self.alarm,
                        door_open=self.door_open, sensor_fault=self.sensor_fault,
                        automatic=self.automatic)
    def read(self, function: int, address: int, count: int):
        with self.lock:
            maps = {
                3: [round(self.setpoint*10), 80, int(self.automatic)],
                4: [round(self.temp*10), int(self.compressor), int(self.alarm), int(self.sensor_fault)],
                1: [int(self.door_open), int(self.sensor_fault)],
                2: [int(self.compressor), int(self.alarm)],
            }
            data = maps[function]
            if count < 1 or count > 125 or address < 0 or address+count > len(data):
                raise ValueError('illegal address')
            return data[address:address+count]
    def write_register(self, address: int, value: int):
        with self.lock:
            if address == 0 and 0 <= value <= 500:
                # VULNERABLE BY DESIGN: PLC accepts dangerous values up to 50 C.
                # Alarm does not independently constrain the setpoint.
                self.setpoint = value/10
            elif address == 2 and value in (0, 1):
                self.automatic = bool(value)
            else:
                raise ValueError('illegal value or read-only address')
    def write_coil(self, address: int, value: int):
        with self.lock:
            if address == 0: self.door_open = bool(value)
            elif address == 1: self.sensor_fault = bool(value)
            else: raise ValueError('illegal address')
