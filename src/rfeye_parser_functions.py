import re
import struct

from Band import Band


RFEYE_FILE_MARKER = 0x55555555

file_header = [('i', 'file_format_version'),
               ('32s', 'file_name')]

block_header = [('i', 'thread_id'),
                ('i', 'block_size'),
                ('i', 'data_type')]

block_trailer = [('i', 'checksum'),
                 ('i', 'marker')]

# Data Type Definitions are 3-tuples of the form:
#     ( Name, Description, [Type Sequence] )
# Where Type Sequence is an array of 2-tuples of the form:
#     (C type, Variable Name)
data_type_definitions = {
    1: ('unit', 'Unit Information',
        [('16s', 'asm'),
         ('i', 'text_len'),
         ('%(text_len)ss', 'text'),
         ('B', 'ant1'),
         ('B', 'ant2'),
         ('B', 'ant3'),
         ('B', 'ant4')
         ]),

    2: ('gps', 'GPS Data',
        [('i', 'time'),
         ('i', 'date'),
         ('H', 'fix'),
         ('H', 'status'),
         ('H', 'sats'),
         ('i', 'lat'),
         ('i', 'long'),
         ('i', 'speed'),
         ('H', 'heading'),
         ('i', 'alt'),
         ]),

    3: ('thread', 'Data Thread Information',
        [('i', 'text_len'),
         ('%(text_len)ss', 'text'),
         ]),

    4: ('data', '8 Bit Spectral Data',
        [('h', 'start'),
         ('h', 'stop'),
         ('b', 'level'),
         ('B', 'antenna'),
         ('B', 'processing'),
         ('B', 'npads'),
         ('i', 'nbytes'),
         ('%(nbytes)dB', 'data'),
         ('%(npads)dB', 'pad'),
         ]),

    5: ('text', 'Free Text',
        [('i', 'text_len'),
         ('%(text_len)ss', 'text'),
         ]),

    6: ('iqdata', '16 Bit I/Q Data',
        [('i', 'start'),
         ('i', 'stop'),
         ('i', 'delta'),
         ('i', 'antenna'),
         ('i', 'samples'),
         ('i', 'nfreqs'),
         ('%(nfreqs)di', 'gains'),
         ('i', 'nvals'),
         ('%(nvals)di', 'iqvals'),
         ]),

    7: ('compressed', 'Compressed Samples',
        [('i', 'start'),
         ('i', 'stop'),
         ('i', 'level'),
         ('i', 'threshold'),
         ('i', 'antenna'),
         ('i', 'processing'),
         ('i', 'loops'),
         ('i', 'nvals'),
         ('i', 'npads'),
         ('i', 'nbytes'),
         ('%(nbytes)dB', 'data'),
         ('%(npads)dB', 'pad'),
         ]),

    8: ('occupancy', 'Occupancy over time',
        [('i', 'start'),
         ('i', 'stop'),
         ('i', 'threshold'),
         ('i', 'time'),
         ('i', 'date'),
         ('i', 'duration'),
         ('i', 'antenna'),
         ('i', 'number'),
         ('i', 'npads'),
         ('i', 'nbytes'),
         ('%(nbytes)dB', 'data'),
         ('%(npads)dB', 'pad'),
         ]),

    9: ('ttext', 'Typed Text',
        [('i', 'type'),
         ('i', 'desc_len'),
         ('%(desc_len)ss', 'dtext'),
         ('i', 'con_len'),
         ('%(con_len)ss', 'ctext'),
         ]),
    }


def open_rfeye_file(filename):
    input_file = open(filename, 'rb')
    return input_file


def parse_rfeye_file(input_file):
    all_data = read_all_data(input_file)
    grouped_data = group_data_by_type(all_data)
    del all_data

    parsed_data = get_all_bands(grouped_data)
    parsed_data.sort(key=lambda x: x.start_freq)

    return parsed_data


#Band info is stored in Data Type 3 (Data Thread Information)
#However, the resolution must be inferred from the data points
def get_all_bands(grouped_data):
    all_bands = []

    for frequency_range, sweeps in grouped_data[4].iteritems():
        resolution = len(sweeps[0]['data'])
        current_band = Band(frequency_range[0], frequency_range[1], resolution)

        for sweep in sweeps:
            start_time = None
            stop_time = None
            measurements = list(sweep['data'])
            current_band.add_scan(start_time, stop_time, measurements)

        all_bands.append(current_band)

    return all_bands


def group_data_by_type(all_data):
    grouped_data = dict()

    for type_identifier in data_type_definitions.keys():
        grouped_data[type_identifier] = []

    for entry in all_data[1]:
        grouped_data[entry[0]].append(entry[1])

    #Group the Measurement data by band
    grouped_data[4] = group_measurements_by_band(grouped_data)

    return grouped_data


def group_measurements_by_band(grouped_data):
    band_measurements = dict()

    for entry in grouped_data[4]:
        frequency_range = (entry['start'], entry['stop'])

        if frequency_range not in band_measurements:
            band_measurements[frequency_range] = []

        band_measurements[frequency_range].append(entry)

    return band_measurements


def read_structure(input_file, type_sequence):
    data = {}
    checksum = 0

    for ctype, variable_name in type_sequence:
        # Replaces '%(Variable Name)d' in the ctype with the value of 'Variable Name' (read previously)
        ctype = ctype % data

        try:
            chunk_size = struct.calcsize(ctype)
        except struct.error:
            print 'read_next {0} {1} {2} {3}'.format(chunk_size, ctype, variable_name, data)

        chunk = input_file.read(chunk_size)
        checksum += sum([ord(byte) for byte in chunk])

        if chunk_size and not chunk:
            raise EOFError

        value = struct.unpack(ctype, chunk)

        if len(value) == 1:
            value = value[0]

        data[variable_name] = value

    return data, checksum


def read_body(input_file, block_type):
    type_sequence = data_type_definitions[block_type][2]
    return read_structure(input_file, type_sequence)


def read_file_header(input_file):
    header_data, header_checksum = read_structure(input_file, file_header)
    return header_data


def read_block_header(input_file):
    return read_structure(input_file, block_header)


def read_block_trailer(input_file):
    block_trailer_data, block_trailer_checksum = read_structure(input_file, block_trailer)
    return block_trailer_data


def set_file_pointer_position(input_file, new_position):
    input_file.seek(new_position)


# From the starting_position, walk the file until you hit the End Of Block Marker
# Where the End Of Block Marker is RFEYE_FILE_MARKER (0x55555555)
def skip_to_marker(input_file, starting_position):
    input_file.seek(starting_position)
    while True:
        value = ord(input_file.read(1))
        if value == 0x55:
            if [ord(byte) for byte in input_file.read(3)] == [0x55, 0x55, 0x55]:
                break


def read_data_block(input_file, position=None):
    if position is not None:
        set_file_pointer_position(input_file, position)
    position = input_file.tell()

    header_data, header_checksum = read_block_header(input_file)
    block_data, block_checksum = read_body(input_file, header_data['data_type'])
    trailer_data = read_block_trailer(input_file)

    calculated_checksum = header_checksum + block_checksum

    if calculated_checksum != trailer_data['checksum']:
        print 'Checksum Comparison Failed! {0} {1} != {2} (delta {3})'.format(position, trailer_data['checksum'],
                                                                              calculated_checksum,
                                                                              calculated_checksum - trailer_data['checksum'])

    if trailer_data['marker'] != RFEYE_FILE_MARKER:
        print 'Marker Failed! {0} != {1}'.format(trailer_data['marker'], RFEYE_FILE_MARKER)
        skip_to_marker(input_file, position)

    return header_data['data_type'], block_data


def read_all_data(input_file):
    header = read_file_header(input_file)
    body = []

    while True:
        try:
            block_type, block_data = read_data_block(input_file)
            body.append([block_type, block_data])
        except EOFError:
            break

    return header, body


def location_from_rfeye_name(filename):
    split_file = filename.split('_')
    return '{0}_{1}'.format(split_file[2], split_file[3])


def file_date_from_rfeye_name(filename):
    numbers = re.findall(r"\d+", filename)
    if len(numbers) == 0:
        return 'Unknown'
    else:
        return '20{0}'.format(numbers[0][:6])