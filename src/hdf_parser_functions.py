#
# Note: This file casts data types from their numpy formats
#       to their vanilla python formats because Avro dislikes
#       numpy datatypes.
#

import re
import h5py

from Band import Band


def open_hdf_file(filename):
    data_file = h5py.File(filename, 'r')
    return data_file


def parse_hdf_file(data_file):
    file_data = get_all_bands(data_file)

    all_data = get_all_data(data_file)
    all_scan_times = get_all_scan_times(data_file)
    for scan_id, complete_sweep in enumerate(all_data):
        for band_id, scan in enumerate(complete_sweep):
            start_time = float(all_scan_times[scan_id][0][band_id])
            end_time = float(all_scan_times[scan_id][1][band_id])
            formatted_scan = [float(measurement) for measurement in scan.tolist()]
            file_data[band_id].add_scan(start_time, end_time, formatted_scan)

    return file_data


def get_all_data(data_file):
    data_group = data_file['/data']

    all_data = []
    for row in data_group:
        all_data.append(row[3])

    return all_data


def get_all_scan_times(data_file):
    data_group = data_file['/data']

    all_scan_times = []
    # Row = [ Start Time, Stop Time ]
    for row in data_group:
        all_scan_times.append([row[0], row[1]])

    return all_scan_times


def get_all_bands(data_file):
    bands_group = data_file['/bands']

    all_bands = []
    # Row = [Starting Frequency, Stopping Frequency, Resolution]
    for row in bands_group:
        current_band = Band(float(row[1]), float(row[2]), int(row[3]))
        all_bands.append(current_band)

    return all_bands
