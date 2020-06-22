import os
from scripts.importjson import loadjson_func
import csv
import pandas as pd

source_dir = '../Data/input/'
meta_file ='../Data/meta/load_table.csv'
df = pd.read_csv(meta_file)


for subdir, dirs, files in os.walk(source_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        file_directory = subdir
        filename = file
        reader = csv.DictReader(open(meta_file))
        if file_path.endswith(".json") and filename not in df['filename']:
            source_file_url = file_path
            with open(meta_file, 'a') as loadtable:
                csv_out = csv.writer(loadtable)
                loadtable.write('{}, {}'.format(filename, loadjson_func(source_file_url)))
                loadtable.write('\n')









