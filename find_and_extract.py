#!/usr/local/bin/python3.6

import os, sys
import datetime
from subprocess import call
from subprocess import check_output
from pathlib import Path
from settings import bin_7z
from settings import downloads_path
from settings import extension

rar_list = []

def find_rars(d_path, extension):
    '''Recursivly checks directories and
    looks for files with .extension, returns dict:
    {absolute_path,
    (list_of_files_with_extension_in_absolute_path)}'''
    ext_dict = {}
    for roots, dirs, files in os.walk(d_path):
        for filename in files:
            if filename.lower().endswith((extension.lower())):
                if ext_dict.get(roots) is None:
                    ext_dict[roots] = []
                ext_dict[roots].append(filename)
    return ext_dict

def is_extracted(directory, filename):
    '''TODO chech file size'''
    wd = os.getcwd()
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
    wd = os.getcwd()
    os.chdir(directory)
    print("Processing ", filename, "... ")
    call([bin_7z, "e", filename])
    os.chdir(wd)

def save_file(log_entry):
    f = "/root/scripts/unrar/extract.log"
    if os.path.exists(f):
        append_or_write = "a"
    else:
        append_or_write = "w"

    f = open(f, append_or_write)
    now = str(datetime.datetime.now())
    msg = (now + " : " + str(log_entry) + "\n")
    f.write(msg)
    f.close()

if __name__ == "__main__":
    pidfile = "/tmp/compressed.pid"
    if Path(pidfile).is_file():
        print ("Process already running, try: ps aux | grep compressed")
        sys.exit()
    else:
        f = open(pidfile, mode="w").close()
        try:
            for k, v in find_rars(downloads_path, extension).items():
                for i in v:
                    while not is_extracted(k, i):
                        msg = ("File: %s extracted" % i)
                        save_file(msg)
                        extract_compressed(k, i)
                    else:
                        print (i, '\t',  ' extracted. ')
        finally:
            os.unlink(pidfile)
