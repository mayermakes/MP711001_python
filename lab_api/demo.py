from psu_device import MP711001
import time
psu = MP711001("192.168.1.100")

psu.set_voltage(1, 5.0)
psu.output_on(1)
print(psu.measure(1))




psu.set_voltage(2, 3.3)
psu.set_current(2, 1.0)
psu.output_on(2)

print(psu.measure(2))

psu.output_off(1)
time.sleep(4)
psu.output_off(2)
