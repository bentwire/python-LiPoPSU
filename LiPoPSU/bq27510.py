import smbus


class bq27510(object):
    def __init__(self, bus):
        pass

    def get_Control(self):
        pass

    def set_Control(self, value):
        pass

    def get_AtRate(self):
        pass

    def set_AtRate(self, value):
        pass

    def get_AtRateTimeToEmpty(self):
        pass

    def get_Temperature(self):
        pass

    def get_Voltage(self):
        pass

    def get_Flags(self):
        pass

    def get_NominalAvailableCapacity(self):
        pass

    def get_FullAvailableCapacity(self):
        pass

    def get_RemainingCapacity(self):
        pass

    def get_FullChargeCapacity(self):
        pass

    def get_AverageCurrent(self):
        pass

    def get_TimeToEmpty(self):
        pass

    def get_TimeToFull(self):
        pass





address   = 0x55
pmaddress = 0x09

bus  = smbus.SMBus(1)

# Enable full 500mA charging in PMIC
bus.write_byte_data(pmaddress, 0x0f, 0x03)


data = bus.read_word_data(address, 0x0e)
print data
data = bus.read_word_data(address, 0x10)
print data
data = bus.read_word_data(address, 0x12)
print data


data = bus.read_word_data(address, 0x2a)
print data
data = bus.read_word_data(address, 0x2c)
print data

data = bus.read_word_data(address, 0x08)
print data
data = bus.read_word_data(address, 0x14)
if data > 32767:
    data -= 65536
print data

data = bus.read_word_data(address, 0x16)
print data
print("Time To Empty: %d:%02d" % (data/60, data%60))
data = bus.read_word_data(address, 0x18)
print data
print("Time To Full:  %d:%02d" % (data/60, data%60))

