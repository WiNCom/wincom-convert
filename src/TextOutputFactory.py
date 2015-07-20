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
        output_file.write('File Name,File Date,Location,Band Count\n')
        output_file.write('{0},{1},{2},{3}\n'.format(session.filename, session.file_date, session.location, session.get_band_count()))

    @staticmethod
    def _write_band(band, output_file):
        output_file.write('Start Frequency,Stop Frequency,Resolution\n')
        output_file.write('{0},{1},{2}\n'.format(band.start_freq, band.stop_freq, band.resolution))
        output_file.write('Start Time,Stop Time,Data\n')
        for scan in band.scans:
            output_file.write('{0},{1},{2}\n'.format(scan.start_time, scan.stop_time, ','.join(str(x) for x in scan.measurements)))

    @staticmethod
    def _write_footer(output_file):
        pass
