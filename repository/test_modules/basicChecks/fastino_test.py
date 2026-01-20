import artiq
from artiq.experiment import *
import numpy as np
import sys
import logging
from artiq.experiment import EnvExperiment
from artiq.experiment import StringValue, BooleanValue,NumberValue
from artiq.experiment import kernel
from artiq.experiment import rpc
import time


class FastinoTest(EnvExperiment): # The name that appears in artiq_dashboard
    def build(self): # defines all of the devices that the experiment (the program) will use - NO @KERNEL SO IT IS NOT RUN ON THE FPGA
        self.setattr_device("core") # the kasli core device
        self.setattr_device("fastino0") # fastino card
        self.setattr_argument("bias_voltage", NumberValue(0.0, unit="V")) 

    



    @kernel
    def run(self): # takes all the prepared values and runs the experiment on the FPGA
        self.core.reset()
        self.fastino0.set_dac(0, self.bias_voltage / 10.0)
        self.fastino0.load()

