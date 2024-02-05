#!/usr/bin/env python3

import pyaudio
p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

print("audio apis:")
for i in range(p.get_host_api_count()):
    device = p.get_host_api_info_by_index(i)
    print(f"{device['index']}: {device['name']}")

print("audio inputs:")


print("audio devices:")
for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    print(f"{device['index']}: {device['name']}")

print("default input:")
print(p.get_default_input_device_info())

print("default output:")
print(p.get_default_output_device_info())
