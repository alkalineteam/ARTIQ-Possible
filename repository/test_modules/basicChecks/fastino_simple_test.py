import artiq
from artiq.experiment import *
import numpy as np
import sys
import logging
from artiq.experiment import EnvExperiment
from artiq.experiment import StringValue, BooleanValue, NumberValue
from artiq.experiment import kernel
from artiq.experiment import rpc
import time


class FastinoTestSimple(EnvExperiment): # The name that appears in artiq_dashboard
    def build(self): # defines all of the devices that the experiment (the program) will use - NO @KERNEL SO IT IS NOT RUN ON THE FPGA
        self.setattr_device("core") # the kasli core device
        self.setattr_device("fastino0") # fastino card
        self.setattr_argument("output_voltage", NumberValue(default=0.05))
        

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        
        self.fastino0.init()
        delay(100*us)
        
        self.fastino0.set_dac(0, self.output_voltage)
        delay(100*us)
        
        self.fastino0.update(0x1)  # update DAC channel 0
        delay(100*us)

