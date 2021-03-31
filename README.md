# py-korad
Korad Test & Measurment Equipment Python Library

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

This is the start of a reposistory to unify the Korad device drivers into a single repository. This is currently under development and notes will be shown below on what support is currently avalible.

**Check out the Wiki for more info**

## KEL103 30A 120V DC Electronic Load
- Ethernet Interface: Currently a work in progress with many features tested and working
- USB Interface: WIP

## KA P Series Power Supplies (ie. KA6003P)
I will most likley pull this from one of the existing Korad Serial libraries.

## KD P Series Power Supplies
Once I have compaired the SCPI command set between this device and the KA series hopefully we will just be able to unify these into a single class. 

## Getting Started

```
from korad import Kel103, KoradUdpComm
comm = KoradUdpComm(local_address, kel_address)
kel = Kel103(comm)
kel.measure_voltage()
```

for battery testing:
```
from korad import Kel103, KoradUdpComm
comm = KoradUdpComm(local_address, kel_address)
kel = Kel103(comm)
test = KelBatteryDischargeTest(kel)
test.setup_for_test(cell_id, set_current, voltage_cutoff)
test.run_test()
test.export_results()
```

## Tests
To run the tests open a terminal in the top-level folder. Run `python .\tests.py`.