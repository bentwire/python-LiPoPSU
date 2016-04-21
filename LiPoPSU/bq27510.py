import time
import logging

log = logging.getLogger(__name__)


class bq27510(object):
    CNTL    = 0x00 # This and AR are the only R/W regs.
    AR      = 0x02
    ARTTE   = 0x04 # From here down the registers are RO.
    TEMP    = 0x06
    VOLT    = 0x08
    FLAGS   = 0x0a
    NAC     = 0x0c
    FAC     = 0x0e
    RM      = 0x10
    FCC     = 0x12
    AI      = 0x14
    TTE     = 0x16
    TTF     = 0x18
    SI      = 0x1a
    STTE    = 0x1c
    MLI     = 0x1e
    MLTTE   = 0x20
    AE      = 0x22
    AP      = 0x24
    TTECP   = 0x26
    RSVD    = 0x28
    CC      = 0x2a
    SOC     = 0x2c

    ADDRESS = 0x55

    def __init__(self, bus, retries = 5):
        self.bus     = bus
        self.retries = retries

    def readReg(self, reg):
        for retry in range(self.retries):
            try:
                return self.bus.read_word_data(bq27510.ADDRESS, reg)
            except Exception as e:
                log.error("Exception during read: %s" % (e))
                time.sleep(0.1)
        else:
            raise Exception("Too many retries on READ.")

    @property
    def Control(self):
        return self.readReg(bq27510.CNTL)

    @Control.setter
    def Control(self, val):
        return self.writeReg(bq27510.CNTL)

    @property
    def Temperature(self):
        return self.readReg(bq27510.TEMP)

    @property
    def Voltage(self):
        voltage = self.readReg(bq27510.VOLT)
        return float(voltage)/1000

    @property
    def Flags(self):
        return self.readReg(bq27510.FLAGS)

    @property
    def NominalAvailableCapacity(self):
        cap = self.readReg(bq27510.NAC)
        return float(cap)/1000

    @property
    def FullAvailableCapacity(self):
        cap = self.readReg(bq27510.FAC)
        return float(cap)/1000

    @property
    def RemainingCapacity(self):
        cap = self.readReg(bq27510.RM)
        return float(cap)/1000

    @property
    def FullChargeCapacity(self):
        cap = self.readReg(bq27510.FCC)
        return float(cap)/1000

    @property
    def AverageCurrent(self):
        current = self.readReg(bq27510.AI)
        if current > 32767:
            current -= 65536
        return float(current)/1000

    @property
    def TimeToEmpty(self):
        return self.readReg(bq27510.TTE)

    @property
    def TimeToFull(self):
        return self.readReg(bq27510.TTF)

    @property
    def StandbyCurrent(self):
        i = self.readReg(bq27510.SI)
        return float(i)/1000

    @property
    def StandbyTimeToEmpty(self):
        return self.readReg(bq27510.STTE)

    @property
    def MaxLoadCurrent(self):
        i = self.readReg(bq27510.MLI)
        return float(i)/1000

    @property
    def MaxLoadTimeToEmpty(self):
        return self.readReg(bq27510.MLTTE)

    @property
    def AvailableEnergy(self):
        ae = self.readReg(bq27510.AE)
        return float(ae)/1000

    @property
    def AveragePower(self):
        ap = self.readReg(bq27510.AP)
        return float(ap)/1000

    @property
    def TTEatConstantPower(self):
        return self.readReg(bq27510.TTECP)

    @property
    def CycleCount(self):
        return self.readReg(bq27510.CC)

    @property
    def StateOfCharge(self):
        return self.readReg(bq27510.SOC)
