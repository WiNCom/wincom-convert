import numpy as np
from Scan import Scan


class Band:
    def __init__(self, start_freq, stop_freq, resolution):
        self.start_freq = start_freq
        self.stop_freq = stop_freq
        self.resolution = resolution
        self.scans = []

    def to_string(self):
        return "Start: {0} Hz\nStop: {1} Hz\nScan Resolution: {2}\n".format(self.start_freq,
                                                                            self.stop_freq, self.resolution)

    def to_numpy(self):
        band_type = np.dtype([('Start Frequency', np.int32), ('Stop Frequency', np.int32), ('Resolution', np.int32)])
        return np.array((self.start_freq, self.stop_freq, self.resolution), dtype=band_type)

    def contains_frequency(self, test_frequency):
        if self.start_freq <= test_frequency <= self.stop_freq:
            return True
        else:
            return False

    def add_scan(self, start_time, stop_time, powers):
        scan = Scan(start_time, stop_time, powers)
        self.scans.append(scan)

    def get_max_power_per_scan(self):
        max_powers = []

        for scan in self.scans:
            max_powers.append(scan.get_max_measurement())

        return max_powers

    def get_min_power_per_scan(self):
        min_powers = []
        for scan in self.scans:
            min_powers.append(scan.get_min_measurement())
        return min_powers

    def get_min_recorded_power(self):
        min_power = float("inf")
        for scan in self.scans:
            min_power = min(scan.get_min_measurement(), min_power)
        return min_power

    def get_max_recorded_power(self):
        max_power = float("-inf")
        for scan in self.scans:
            max_power = max(scan.get_max_measurement(), max_power)
        return max_power

    def get_datetimes_of_max(self):
        scans_including = []
        max_power = self.get_max_recorded_power()
        for scan in self.scans:
            if max_power in scan.get_measurements():
                scans_including.append((scan.get_start_datetime(), scan.get_stop_datetime()))
        return scans_including

    def get_datetimes_of_min(self):
        scans_including = []
        min_power = self.get_min_recorded_power()
        for scan in self.scans:
            if min_power in scan.get_measurements():
                scans_including.append((scan.get_start_datetime(), scan.get_stop_datetime()))
        return scans_including

    def scans_to_numpy(self):
        data = []
        for scan in self.scans:
            data.append(scan.to_numpy())
        return np.array(data)
