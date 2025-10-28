import numpy as np
from artiq.experiment import *

class PT100SamplerReader(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("sampler0")

        self.setattr_argument("sample_delay", NumberValue(default=100*ms, unit="ms"))
        self.setattr_argument("num_samples", NumberValue(default=500))
        self.setattr_argument("alpha1", NumberValue(default=397))
        self.setattr_argument("alpha2", NumberValue(default=385))

    def prepare(self):
        self.Vref = 5.0
        self.I_pt100 = 0.001  # 1 mA
        self.GAIN = 10.0
        self.R0 = 100.0
        self.alpha1 = self.alpha1 / 1e5
        self.alpha2 = self.alpha2 / 1e5

        self.samples_ch2 = []  # Sampler channel 2 for PT100
        self.temperatures_ch2 = []
        self.samples_ch4 = []  # Sampler channel 4 for PT100
        self.temperatures_ch4 = []

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        num_samples = int(self.num_samples)
        self.sampler0.init()
        
        delay(10*ms)

        samples = [[0.0]*8 for _ in range(num_samples)]

        samples_ch2 = [0.0]*num_samples
        temperatures_ch2 = [0.0]*num_samples
        samples_ch4 = [0.0]*num_samples
        temperatures_ch4 = [0.0]*num_samples

        for i in range(num_samples):
            self.sampler0.sample(samples[i])
            delay(self.sample_delay)

        # Extract and convert channel 2 data (PT100 on sampler channel 2)
        for i in range(num_samples):
            v_out_ch2 = samples[i][2]  # channel 2
            v_pt100_ch2 = v_out_ch2 / self.GAIN
            r_pt100_ch2 = v_pt100_ch2 / self.I_pt100
            temperature_ch2 = (r_pt100_ch2 - self.R0) / (self.R0 * self.alpha1)

            samples_ch2[i] = v_out_ch2
            temperatures_ch2[i] = temperature_ch2

        # Extract and convert channel 4 data (PT100 on sampler channel 4)
        for i in range(num_samples):
            v_out_ch4 = samples[i][4]  # channel 4
            v_pt100_ch4 = v_out_ch4 / self.GAIN
            r_pt100_ch4 = v_pt100_ch4 / self.I_pt100
            temperature_ch4 = (r_pt100_ch4 - self.R0) / (self.R0 * self.alpha2)

            samples_ch4[i] = v_out_ch4
            temperatures_ch4[i] = temperature_ch4

        # Save datasets
        self.set_dataset("pt100_voltages_ch2", samples_ch2, broadcast=True, archive=True)
        self.set_dataset("pt100_temperatures_ch2", temperatures_ch2, broadcast=True, archive=True)
        self.set_dataset("pt100_voltages_ch4", samples_ch4, broadcast=True, archive=True)
        self.set_dataset("pt100_temperatures_ch4", temperatures_ch4, broadcast=True, archive=True)
        self.set_dataset("sample_index", list(range(num_samples)), broadcast=True, archive=True)

        print("PT100 sampling complete.")
