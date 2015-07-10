from Scan import Scan


class Band:
    def __init__(self, start_freq, stop_freq, resolution):
        self.start_freq = start_freq
        self.stop_freq = stop_freq
        self.resolution = resolution
        self.scans = []

    def get_starting_frequency(self):
        return self.start_freq

    def get_stopping_frequency(self):
        return self.stop_freq

    def get_resolution(self):
        return self.resolution

    def to_string(self):
        return "Start: {0} Hz\nStop: {1} Hz\nScan Resolution: {2}\n".format(self.start_freq,
                                                                            self.stop_freq, self.resolution)

    def to_list(self):
        return [self.start_freq, self.stop_freq, self.resolution]

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

    def get_plot_array(self):
        time_slices = []
        powers = []
        time_slice = 0
        for scan in self.scans:
            if scan.get_start_time() is None:
                time_slices.append(time_slice)
                time_slice += 1
            else:
                time_slices.append(scan.get_start_time())
            powers.append(scan.get_avg_measurement())
        return time_slices, powers

    def to_data_array(self):
        data = []
        scan_count = 1
        for scan in self.scans:
            row = []
            row.append(scan_count)
            row.append(scan.get_start_datetime())
            row.append(scan.get_stop_datetime())
            row += scan.get_measurements()
            scan_count += 1
            data.append(row)
        return data

    def to_avro(self):
        scans = []
        for scan in self.scans:
            scans.append(scan.to_avro())

        return dict({
           'start_freq': self.start_freq,
           'stop_freq': self.stop_freq,
           'resolution': self.resolution,
           'scans': scans,
        })