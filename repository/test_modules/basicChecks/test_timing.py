import logging
from artiq.experiment import EnvExperiment
from artiq.experiment import kernel
from artiq.experiment import delay
from artiq.coredevice.core import Core
from artiq.experiment import *
from artiq.coredevice.ttl import TTLOut
from numpy import int64, int32
import numpy as np
from artiq.coredevice import ad9910

logger = logging.getLogger(__name__)

class test_timing(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.core: Core

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        
        print("waiting 400ms...")
        t1 = self.core.get_rtio_counter_mu()
        delay(500*ms)
        delay(-100*ms)
        t2 = self.core.get_rtio_counter_mu()
        print((t2-t1), "ms")

        print("waiting 1 second....")
        t3 = self.core.get_rtio_counter_mu()
        delay(1000*ms)
        t4 = self.core.get_rtio_counter_mu()
        print((t4-t3), "ms")

        print("Timing test is done")