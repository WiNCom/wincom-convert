import gzip


class TextOutputFactory:
    def __init__(self):
        pass

    def save_session_to_csv(self, session, output_file_name):
        print '[Writing] Writing File: {0}'.format(output_file_name)
        output_file = gzip.open(output_file_name, 'w')
        self._write_session_to_file(session, output_file)
        output_file.close()
        print '[Writing] File Writen Successfully!'

    def _write_session_to_file(self, session, output_file):
        print '[Writing] Writing Header...'
        self._write_header(session, output_file)

        current_band = 1
        total_bands = session.get_band_count()
        for band in session.bands:
            print '[Writing] Writing Band {0}/{1}...'.format(current_band, total_bands)
            self._write_band(band, output_file)
            current_band += 1

        print '[Writing] Writing Footer...'
        self._write_footer(output_file)

    @staticmethod
    def _write_header(session, output_file):
        header = 'File Name,File Date,Location,Band Count\n'
        header += '{0},{1},{2},{3}\n'.format(session.filename, session.file_date, session.location, session.get_band_count())
        header += '\n'
        output_file.write(header)

    @staticmethod
    def _write_band(band, output_file):
        band_data = 'Start Frequency,Stop Frequency,Resolution\n'
        band_data += '{0},{1},{2}\n'.format(band.start_freq, band.stop_freq, band.resolution)
        band_data += '\n'
        band_data += 'Start Time,Stop Time,Data\n'
        for scan in band.scans:
            band_data += '{0},{1},{2}\n'.format(scan.start_time, scan.stop_time, ','.join(str(x) for x in scan.measurements))
        band_data += '\n'
        output_file.write(band_data)

    @staticmethod
    def _write_footer(output_file):
        pass
