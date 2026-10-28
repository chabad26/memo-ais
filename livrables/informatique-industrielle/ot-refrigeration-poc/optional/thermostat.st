(* IEC 61131-3 illustrative logic only. NOT deployed/tested in OpenPLC.
   I/O declarations and mapping depend on the selected OpenPLC target.
   Physical process feedback and timer must be provided by external systems. *)
PROGRAM RefrigerationThermostat
VAR
    Temperature : REAL := 5.0;
    Setpoint : REAL := 4.0;
    SensorFault : BOOL := FALSE;
    Compressor : BOOL := FALSE;
    HighTemperature : BOOL := FALSE;
END_VAR
IF SensorFault THEN
    Compressor := FALSE;
ELSIF Temperature >= Setpoint + 0.5 THEN
    Compressor := TRUE;
ELSIF Temperature <= Setpoint - 0.5 THEN
    Compressor := FALSE;
END_IF;
HighTemperature := Temperature > 8.0;
END_PROGRAM
