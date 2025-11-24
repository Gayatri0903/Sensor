from vl53l5cx import VL53L5CX
import time

# Create sensor object
sensor = VL53L5CX()

# Initialize sensor, upload firmware
sensor.init()

# Start ranging
sensor.start_ranging()

print("Reading RAW VL53LDK data continuously... Press CTRL+C to stop.\n")

try:
    while True:
        if sensor.check_data_ready():
            data = sensor.get_ranging_data()

            # RAW DATA = 32x32 matrix of distances
            raw = data.distance_mm   # list of 32 lists, each with 32 values

            # Print center zone as example
            center = raw[16][16]
            print("Center Zone:", center, "mm")

            # To print full raw grid:
            # for row in raw:
            #     print(row)

        time.sleep(0.02)

except KeyboardInterrupt:
    sensor.stop_ranging()
    print("\nStopped.")