import h5py

class HDFOutputFactory:
    def __init__(self):
        pass

    def save_session_to_hdf5(self, session, output_file_name):
        hdf5_file = h5py.File(output_file_name, 'w')
        self.create_session_group(hdf5_file, session)
        self.create_bands_group(hdf5_file, session)
        hdf5_file.close()

    def create_session_group(self, hdf5_file, session):
        self.create_band_plan_group(hdf5_file, session)
        hdf5_file['/session'].attrs['date'] = session.get_iso_date()
        hdf5_file['/session'].attrs['location'] = session.location

    def create_bands_group(self, hdf5_file, session):
        band_id = 0
        for band in session.bands:
            dataset = '/bands/band_{0}'.format(band_id)
            hdf5_file['{0}/scans'.format(dataset)] = band.scans_to_numpy()
            hdf5_file[dataset].attrs['start_freq'] = band.start_freq
            hdf5_file[dataset].attrs['stop_freq'] = band.stop_freq
            hdf5_file[dataset].attrs['resolution'] = band.resolution
            band_id += 1

    def create_band_plan_group(self, hdf5_file, session):
        bands = session.get_bands()
        hdf5_file['/session/band_plan'] = bands
