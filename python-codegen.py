import subprocess

__author__ = 'Mike McMahon'

import sys
import datetime
import os

CODEGEN_DROP = 'C:\\Codegen\\'
CODEGEN_EXE = 'C:\\Codegen\\'
CODEGEN_PROCESSED = 'list'
CODEGEN_JSON = 'json'


def get_music(path, dir_contents):
    mp3s = []
    other = []
    check_dirs = []
    for d_c in dir_contents:
        full_path = os.path.join(path, d_c)
        if os.path.isdir(full_path):
            check_dirs.append(full_path)
        else:
            mp3s.append(full_path)
    else:
        for cd in check_dirs:
            other += get_music(cd, os.listdir(cd))

    return mp3s + other


def main():
    argc, args = len(sys.argv), sys.argv
    if argc < 2:
        print "Please specify a path to look for music"
        return

    path = args[1]

    if not os.path.isdir(path):
        print "Please specify a dir"
        return

    print "Processing {0}".format(path)

    files = os.listdir(path)
    mp3s = get_music(path, files)

    for m in mp3s:
        print m

    mp3s = [m + '\n' for m in mp3s]


    out_filename = '{0}-file_list.txt'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    out_filepath = os.path.join(CODEGEN_DROP, out_filename)
    with open(out_filepath, 'w') as out_file:
        out_file.writelines(mp3s)

    dest_filepath = os.path.join(CODEGEN_DROP, CODEGEN_JSON,
                                 datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-to_ingest.json')
    with open(dest_filepath, 'w') as output:
        with open(out_filepath) as ingest:
            subprocess.call([os.path.join(CODEGEN_EXE, 'codegen.exe'), '-s'], stdin=ingest, stdout=output)

    os.rename(out_filepath, os.path.join(CODEGEN_DROP, CODEGEN_PROCESSED, out_filename))

if __name__ == '__main__':
    main()
