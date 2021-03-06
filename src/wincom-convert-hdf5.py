import sys

from os import path
from SessionFactory import SessionFactory
from HDFOutputFactory import HDFOutputFactory


def parse_file(input_file):
    print("[Processing] Creating Session Factory")
    session_factory = SessionFactory()
    hdf_factory = HDFOutputFactory()
    parse_map = {
        'bin': session_factory.session_from_rfeye_file,
        'hdf5': session_factory.session_from_hdf_file,
        'hdf': session_factory.session_from_hdf_file,
    }

    print("[Processing] Parsing File " + input_file)
    file_name = path.split(input_file)[1]
    file_type = file_name.split('.')[-1]

    print("[Processing] Parsing as '{0}' File".format(file_type))
    if file_type not in parse_map:
        print("[Error] '{0}' is an unsupported file type!".format(file_type))
        return

    parser = parse_map[file_type]
    session = parser(input_file)

    print("[Processing] File Successfully Parsed")
    output_base_name = input_file.split('.')[0]
    output_name = '{0}.hdf5'.format(output_base_name)
    hdf_factory.save_session_to_hdf5(session, output_name)
    print("[Complete] Output File Generated Successfully!")


if __name__ == '__main__':
    arguments = sys.argv[1:]
    arguments = ['Z:/Data/Wincom/RFeye/RFeye_WiFiUS_HP_141222_001725.bin']
    if len(arguments) != 1:
        print("[Error] You didn't include any arguments!\n" +
              "[Usage] python wincom-convert.py /your/input_file/here")
    else:
        parse_file(arguments[0])
