import numpy as np
from datetime import datetime

class RTH1004_CSV():
    def __init__(self, filename):
        with open(filename, "rt") as f:
            header_raw = [next(f).split(";") for _ in range(22)]
            self.samples_raw = np.genfromtxt(f, delimiter=";", skip_header=22)
        self.header = header = {row[0]: row[1:] for row in header_raw}

        assert header["Model"][0] == "RTH1004", 'Device model must be "RTH1004"'
        self.serial_number = int(header["SerialNumber"][0])
        self.firmware_version = header["Firmware Version"][0].strip("\'")
        date_str = str(header["Acquisition Time Stamp"])[0][:-3]
        self.acquisition_time_stamp = datetime.fromisoformat(date_str)
        self.waveform_type = header["Waveform Type"][0]
        self.acquisition_mode = header["Acquisition Mode"][0]
        self.horizontal_unit = header["Acquisition Unit"][0]
        self.horizontal_scale = float(header["Horizontal Scale"][0])
        self.horizontal_position = float(header["Horizontal Position"][0])
        self.reference_point_percent = int(header["Reference Point"][0][0:3])
        self.sample_interval = float(header["Sample Interval"][0])
        self.record_length = int(header["Record Length"][0])

        self.probe_settings = header["Probe Setting"]
        self.vertical_units = header["Vertical Unit"]
        self.vertical_scales = [float(v) for v in header["Vertical Scale"]]
        self.vertical_positions = [float(v) for v in header["Vertical Position"]]
        self.vertical_offsets = [float(v) for v in header["Vertical Offset"]]
        self.history_index = [int(v) for v in header["History Index"]]
        self.history_time_stamps = [float(v) for v in header["History Time Stamp"]]

    def set_zoom(self, t_start: float, t_end: float):
        self.t_start = t_start
        self.t_end = t_end
        time = self.samples_raw[:][0]
        self.idx_start = np.where(time >= t_start)[0][0]
        self.idx_end = np.where(time <= t_end)[0][-1]

    @property
    def time_zoomed(self) -> np.Array:
        return self.samples_raw[self.idx_start:self.idx_end].T[0]

    @property
    def chs_zoomed(self) -> np.Array:
        return self.samples_raw[self.idx_start:self.idx_end].T[1:]


# Model;RTH1004
# SerialNumber;103752
# Firmware Version;'1.80.3.4'

# Acquisition Time Stamp;2023-01-23 12:08:02.423888073;2023-01-23 12:08:02.423888073;2023-01-23 12:08:02.423888073;2023-01-23 12:08:02.423888073
# Waveform Type;ANALOG;;;
# Acquisition Mode;PEAK;;;
# Horizontal Unit;s;;;
# Horizontal Scale;5e-07;;;
# Horizontal Position;-2.504e-07;;;
# Reference Point;50 %;;;
# Sample Interval;8e-10;;;
# Record Length;6250;;;
# Probe Setting;'100:1';'100:1';'10:1';'0.1 V/A'
# Vertical Unit;V;V;V;A
# Vertical Scale;5;5;200;5
# Vertical Position;-1;-1;-1;1
# Vertical Offset;0;0;0;0
# History Index;0;0;0;0
# History Time Stamp;0.000000000000;0.000000000000;0.000000000000;0.000000000000
# ;;;;
# TIME;CH1;CH2;CH3;CH4
# -2.7504e-06;16.9216;0.529412;5.4902;0.411765
# -2.7496e-06;16.7647;0.45098;5.4902;0.411765