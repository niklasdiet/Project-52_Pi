import time
import json
from machine import Pin, I2C, ADC

max_val = None
min_val = None

soil = ADC(Pin(26)) # Soil moisture PIN reference

print("Dry")
time.sleep(10)
max_val = soil.read_u16()
print("------{:>5}\t{:>5}".format("raw", "v"))
for x in range(0, 10):
    if soil.read_u16() > max_val:
        max_val = soil.read_u16()
        print("CHAN 0: "+"{:>5}\t".format(soil.read_u16()))
    time.sleep(0.5)
print('\n')
print("Wet")
time.sleep(10)
min_val = soil.read_u16()
print("------{:>5}\t{:>5}".format("raw", "v"))
for x in range(0, 10):
    if soil.read_u16() < min_val:
        min_val = soil.read_u16()
    print("CHAN 0: "+"{:>5}\t".format(soil.read_u16()))
    time.sleep(0.5)
config_data = dict()
config_data["full_saturation"] = min_val
config_data["zero_saturation"] = max_val
with open('cap_config.json', 'w') as outfile:
    json.dump(config_data, outfile)
print('\n')
print(config_data)