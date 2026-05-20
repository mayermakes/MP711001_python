# MP711001_python
a web interface / usage example to control the MP711001 programmable power supply via web interface /python


psu_device/
 ├── __init__.py
 ├── mp711001.py   ← driver (core device)
 └── flask_app.py  ← optional web UI wrapper


 Usage:

from psu_device import MP711001

psu = MP711001("192.168.1.100")

#device.command(channel,value)

psu.set_voltage(1, 3.3)
psu.set_current(1, 1.0)
psu.output_on(1)

print(psu.measure(1))
