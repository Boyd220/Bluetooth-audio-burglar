import bluetooth

while True:
    nearby_devices = bluetooth.discover_devices()
    print ("found device:  ", nearby_devices)
