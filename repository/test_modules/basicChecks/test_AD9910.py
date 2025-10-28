from artiq.experiment import *
from numpy import int64, int32

class TestAD9910(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        # Only use the first Urukul card's channels
        self.dds_channels = [
            self.get_device("urukul0_ch0"),
            self.get_device("urukul0_ch1"),
            self.get_device("urukul0_ch2"),
            self.get_device("urukul0_ch3"),
        ]
        # Only initialize the first Urukul card
        self.urukul0 = self.get_device("urukul0_cpld")
        self.setattr_argument("Number_of_pulse", NumberValue(default=10))
        self.setattr_argument("Pulse_width", NumberValue(default=1000)) 

    @kernel
    def run(self):
        self.core.break_realtime()

        self.urukul0.init()
        for dds in self.dds_channels:
            dds.init()
            dds.set_att(0.0)

        for i in range(int(self.Number_of_pulse)):
            for dds in self.dds_channels:
                dds.sw.on()
                dds.set(frequency=80*MHz, amplitude=0.06)

            delay(self.Pulse_width * ms)

            for dds in self.dds_channels:
                dds.sw.off()

            delay(self.Pulse_width * ms)

            # Uncomment the next line if you still get underflows
            # self.core.break_realtime()
        print("Test completed successfully.")
