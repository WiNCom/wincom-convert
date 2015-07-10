class RecordingSession:
    def __init__(self, filename, file_date, location, bands):
        self.filename = filename
        self.file_date = file_date
        self.location = location
        self.bands = bands

    def print_bands(self):
        for band in self.bands:
            print(band.to_string())

    def get_bands(self):
        bands = []
        for band in self.bands:
            bands.append(band.to_list())
        return bands

    def get_band_count(self):
        return len(self.bands)

    def get_scan_count(self):
        return len(self.scan_times)

    def get_band_summary(self):
        summary = 'All Bands:\n'
        band_id = 0
        for band in self.bands:
            summary = summary + '[{0}]\n'.format(band_id) + band.to_string()
            band_id += 1
        return summary

    def get_band_for_frequency(self, frequency):
        for band in self.bands:
            if band.contains_frequency(frequency):
                return band

        return None

    def band_to_csv(self, band_id):
        band = self.bands[band_id]
        return band.to_data_array()

    def band_to_plot_array(self, band_id):
        band = self.bands[band_id]
        time_slices, avg_powers = band.get_plot_array()
        return time_slices, avg_powers

    def to_avro(self):
        bands = []
        for band in self.bands:
            bands.append(band.to_avro())

        return dict({
            'filename': self.filename,
            'date': self.file_date,
            'location': self.location,
            'bands': bands,
        })