import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x29

def write_reg(reg, val):
    bus.write_byte_data(ADDR, reg, val)

def read_reg(reg):
    return bus.read_byte_data(ADDR, reg)

def read_reg_16(reg):
    high = bus.read_byte_data(ADDR, reg)
    low  = bus.read_byte_data(ADDR, reg + 1)
    return (high << 8) | low

# ----------------------------------------------------
# SENSOR INIT  (Safe minimal init – no invalid regs)
# ----------------------------------------------------
def sensor_init():
    # Soft-reset
    write_reg(0x00, 0x00)    # SYSRANGE_START idle
    write_reg(0x0B, 0x01)    # CLEAR INTERRUPTS
    time.sleep(0.01)

    # Continuous ranging mode
    write_reg(0x00, 0x02)    # bit1 = back-to-back (continuous)
    print("VL53L0X ready!")

# ----------------------------------------------------
# READ RAW + DISTANCE
# ----------------------------------------------------
def read_distance():
    # Wait for measurement ready
    while True:
        status = read_reg(0x13)   # RESULT_INTERRUPT_STATUS
        if (status & 0x07) != 0:
            break
        time.sleep(0.005)

    # Read raw ambient & signal
    ambient = read_reg_16(0xBC)   # RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN
    signal  = read_reg_16(0xC0)   # RESULT_CORE_RANGING_TOTAL_EVENTS_RTN

    # Read distance result
    dist = read_reg_16(0x1E)      # Official distance output register

    # Clear interrupt
    write_reg(0x0B, 0x01)

    return ambient, signal, dist

# ----------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------
sensor_init()

while True:
    ambient, signal, dist = read_distance()
    print(f"Ambient={ambient} | Signal={signal} | Distance={dist} mm")
    time.sleep(0.1)