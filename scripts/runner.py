import os
from scripts.importjson import loadjson_func
import csv


source_dir = '../Data/input/'
meta_file ='../Data/meta/load_table.csv'
exiting_filenames = []

#load meta file for checks
with open(meta_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        exiting_filenames.append(row.get('filename'))



for subdir, dirs, files in os.walk(source_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        file_directory = subdir
        filename = file
        reader = csv.DictReader(open(meta_file))
        #duplicate file checker
        if filename in exiting_filenames:
            print("File {} loaded already".format(filename))
        #call load file
        elif file_path.endswith(".json") :
            source_file_url = file_path
            with open(meta_file, 'a') as loadtable:
                csv_out = csv.writer(loadtable)
                print("File {} is currently loading".format(filename))
                loadtable.write('{}, {}'.format(filename, loadjson_func(source_file_url)))
                print("File {} is done loading".format(filename))
                loadtable.write('\n')