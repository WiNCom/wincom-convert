import re
from datetime import datetime

LOCATION_MAP = {
    'IITSO': 'IIT Spectrum Observatory',
    'TOWER': 'IIT Spectrum Observatory',
    'Chicago': 'Mobile - Chicago',
    'Harbor': 'Harbor Point',
    'HP': 'Harbor Point',
}


def site_from_name(filename):
    split_file = filename.split('_')

    for token in split_file:
        if token in LOCATION_MAP:
            return LOCATION_MAP[token]

    return 'Unknown'


def date_from_name(filename):
    if filename.split('.')[-1] == 'bin':
        return file_date_from_rfeye_name(filename)
    else:
        return file_date_from_hdf_name(filename)


def file_date_from_rfeye_name(filename):
    numbers = re.findall(r"\d+", filename)
    if len(numbers) == 0:
        return 'Unknown'
    else:
        file_date = '20{0}'.format(numbers[0][:6])
        return datetime.strptime(file_date, "%Y%m%d")


def file_date_from_hdf_name(filename):
    numbers = re.findall(r"\d+", filename)
    if len(numbers) == 0:
        return 'Unknown'
    else:
        file_date = numbers[0][:8]
        return datetime.strptime(file_date, "%Y%m%d")


def format_from_name(file_to_store):
    extension = file_to_store.split('.')[-1]
    if extension == 'bin':
        return 'RFEye'
    else:
        return 'HDF5'
