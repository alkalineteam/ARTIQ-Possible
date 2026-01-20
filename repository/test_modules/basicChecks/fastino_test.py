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


class FastinoTest(EnvExperiment): # The name that appears in artiq_dashboard
    def build(self): # defines all of the devices that the experiment (the program) will use - NO @KERNEL SO IT IS NOT RUN ON THE FPGA
        self.setattr_device("core") # the kasli core device
        self.setattr_device("fastino0") # fastino card
        self.setattr_device("sampler0")  #
        

    @kernel
    def run(self): # takes all the prepared values and runs the experiment on the FPGA
        self.core.reset()
        self.sampler0.init()
        num_samples=1000
        # Continuous loop - samples and outputs repeatedly
        for _ in range(num_samples):  # Change 1000 to desired number of iterations
            # Read from sampler0 ADC - reads voltage from input channels
            sampler_data = [0.0, 0.0]
            self.sampler0.sample(sampler_data)
            input_voltage = sampler_data[0]  # Get reading from first channel
            
            # Set fastino output based on sampler input voltage
            # Scale the input to control the output
            output_voltage = input_voltage * 0.5
            
            self.fastino0.set_dac(0, output_voltage / 10.0)
            self.fastino0.load()

