import numpy as np
from datetime import datetime
from scipy.ndimage import uniform_filter1d, median_filter

class RTH1004_DATA():
    """Evaluate Rohde + Schwarz RTH 1004 series oscilloscope save data

    2023-01-27 Ulrich Lukas
    """
    def __init__(self, filename: str=None):
        if filename is not None:
            self.read_csv(filename)
            self.set_viewport()
    
    def read_csv(self, filename: str):
        """Read scope data from CSV savefile.

        The contained oscilloscope settings and sample data
        can then be read by means of instance attributes and properties.
        """
        with open(filename, "rt") as f:
            header_raw = [next(f).rstrip().split(";") for _ in range(20)]
            # self.samples_raw = np.genfromtxt(f, delimiter=";", skip_header=22)
            # First 20 lines are already stripped from above..
            self.samples_raw = np.genfromtxt(f, delimiter=";", skip_header=2)
        header = {row[0]: row[1:] for row in header_raw}

        assert header["Model"][0] == "RTH1004", 'Device model must be "RTH1004"'
        self.serial_number = int(header["SerialNumber"][0])
        self.firmware_version = header["Firmware Version"][0].strip("\'")
        date_str = header["Acquisition Time Stamp"][0][:-3]
        self.acquisition_time_stamp = datetime.fromisoformat(date_str)
        self.waveform_type = header["Waveform Type"][0]
        self.acquisition_mode = header["Acquisition Mode"][0]
        self.horizontal_unit = header["Horizontal Unit"][0]
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

    def set_viewport(self, t_start: float = None, t_end: float = None):
        """Set self.idx_start and self.idx_end defining the current viewport
        
        If t_start and t_end are given, the indices are located by searching
        the time log values for the respective values.
        
        Without both parameters, the viewport is reset to the full extent.
        """
        time = self.samples_raw[:, 0]
        if None in (t_start, t_end):
            self.t_start = time[0]
            self.t_end = time[-1]
            self.idx_start = 0
            self.idx_end = self.record_length - 1
        else:
            self.t_start = t_start
            self.t_end = t_end
            self.idx_start = np.where(time >= t_start)[0][0]
            self.idx_end = np.where(time <= t_end)[0][-1]

    @property
    def time(self) -> np.ndarray:
        return self.samples_raw[:, 0]

    @property
    def ch1(self) -> np.ndarray:
        return self.samples_raw[:, 1]

    @property
    def ch2(self) -> np.ndarray:
        return self.samples_raw[:, 2]

    @property
    def ch3(self) -> np.ndarray:
        return self.samples_raw[:, 3]

    @property
    def ch4(self) -> np.ndarray:
        return self.samples_raw[:, 4]

    @property
    def chs(self) -> np.ndarray:
        return self.samples_raw.T[1:]

    @property
    def time_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end][:, 0]

    @property
    def ch1_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end][:, 1]

    @property
    def ch2_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end][:, 2]

    @property
    def ch3_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end][:, 3]

    @property
    def ch4_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end][:, 4]

    @property
    def chs_zoomed(self) -> np.ndarray:
        return self.samples_raw[self.idx_start:self.idx_end].T[1:]

    def filter_average(self,
                       samples: np.ndarray,
                       size: int,
                       mode: str = "nearest"
                       ) -> np.ndarray:
        """Applies a moving average of [size] input samples.
        
        The output array has the same shape as the input.
        """
        # Roughly the same results but slower:
        # return np.convolve(samples, np.ones(size)/size, 'same')
        return uniform_filter1d(samples, size, mode=mode)

    def do_time_derivative(self,
                           samples: np.ndarray,
                           filter_avg: int = 1
                           ) -> np.ndarray:
        """Returns the first derivative by time of the waveform.
        
        This takes into account the sampling period as defined by
        self.sample_interval.
        
        The first value is repeated once to make the output the
        same shape as the original input samples array.

        For noisy input data (which is the usual case), setting
        filter_avg to an appropriate number of samples
        yields a realistically smooth output waveform.
        """
        if filter_avg > 1:
            samples = self.filter_average(samples, filter_avg)
        return np.ediff1d(
            samples,
            to_begin = samples[1] - samples[0]
        ) / self.sample_interval
    
    def do_time_integral(self, samples: np.ndarray) -> np.ndarray:
        return np.cumsum(samples * self.sample_interval)




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