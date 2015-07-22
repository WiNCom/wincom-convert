import datetime
import numpy as np


class Scan:
    def __init__(self, start_time, stop_time, measurements):
        self.start_time = start_time
        self.stop_time = stop_time
        self.measurements = np.array(measurements, dtype=np.float32)

    def get_iso_start(self):
        if self.start_time is None:
            return 'Unknown'
        else:
            return datetime.datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_iso_stop(self):
        if self.stop_time is None:
            return 'Unknown'
        else:
            return datetime.datetime.fromtimestamp(self.stop_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_measurements(self):
        return self.measurements

    def get_max_measurement(self):
        return np.max(self.measurements)

    def get_min_measurement(self):
        return np.min(self.measurements)

    def get_avg_measurement(self):
        return np.mean(self.measurements)

    def to_numpy(self):
        scan_type = np.dtype([('Start Time', np.str_, 20), ('Stop Time', np.str_, 20), ('Measurements', np.float32, (len(self.measurements),))])
        return np.array((self.get_iso_start(), self.get_iso_stop(), self.measurements), dtype=scan_type)