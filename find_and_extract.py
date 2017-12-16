#!/usr/local/bin/python3.6

import os
import datetime
from subprocess import call
from subprocess import check_output
from settings import bin_7z
from settings import downloads_path

rar_list = []
wd = os.getcwd()

def find_rars(d_path):
    '''Recursivly checks directories and
    looks for hardcoded '.rar' files
    returns dictionary
    {abs path to rar file:,rar file name}'''
    rar_dict = {}
    for roots, dirs, files in os.walk(d_path):
        for filename in files:
            if filename.lower().endswith(('.rar')):
                rar_dict[roots] = filename
    return rar_dict

def is_extracted(directory, filename):
    '''TODO chech file size'''
    os.chdir(directory)
    list_extracted = check_output([bin_7z, 'lb', filename]).splitlines()
    if len(list_extracted) > 0:
        if os.path.isfile(list_extracted[0]):
            os.chdir(wd)
            return True
        else:
            os.chdir(wd)
            return False

def extract_compressed(directory, filename):
    '''TODO exit code handling'''
    os.chdir(directory)
    print("Processing ", filename, "... ")
    call([bin_7z, 'e', filename])
    os.chdir(wd)


def save_file(log_entry):
    f = wd + '/extract.log'
    if os.path.exists(f):
        append_or_write = "a"
    else:
        append_or_write = "w"

    f = open(f, append_or_write)
    now = str(datetime.datetime.now())
    msg = (now + " : " + str(log_entry))
    f.write(msg)
    f.close()

if __name__ == "__main__":
    for k, v in find_rars(downloads_path).items():
        while not is_extracted(k, v):
            msg = (v, 'exctracted')
            save_file(msg)
            extract_compressed(k, v)
        else:
            print (v, '\t',  ' extracted. ')
