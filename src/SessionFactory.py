from os import path

from file_fns import *
from hdf_parser_functions import *
from rfeye_parser_functions import *
from RecordingSession import RecordingSession


class SessionFactory:
    def __init__(self):
        return

    def session_from_hdf_file(self, input_path):
        filename = self.filename_from_path(input_path)
        file_date = file_date_from_hdf_name(filename)
        location = site_from_name(filename)
        data_file = open_hdf_file(input_path)
        bands = parse_hdf_file(data_file)
        return RecordingSession(filename, file_date, location, bands)

    def session_from_rfeye_file(self, input_path):
        filename = self.filename_from_path(input_path)
        file_date = file_date_from_rfeye_name(filename)
        location = site_from_name(filename)
        data_file = open_rfeye_file(input_path)
        bands = parse_rfeye_file(data_file)
        return RecordingSession(filename, file_date, location, bands)

    def filename_from_path(self, filepath):
        return path.split(filepath)[1]