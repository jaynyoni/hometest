WhereIsMyTransportHomeTest

This is a python script to load json files from journey posts, stops and timetables calls as required by the Data Science team.

The script loads the files in the /Data/input path into the /Data/output folder into a json file called events_summary.json in the format requested. The /Data/meta is a folder with the file load_table.csv which acts as a meta table to keep record count of files loaded to avoid loading the same files everytime you call the runner.

The python script will only work in an environment with python 3.7 or above. The assumption is that you already have a process that is writing the log files into the input folder which is a subfolder for the directory Data.


You can call the runner.py to run when is root folder of project as below :

"../hometest/venv/bin/python" "../hometest/scripts/runner.py"

The runner script will :
scan through the /Data/input folder to get all filenames in the directory. Then it will check if any of the filenames have being loaded already by comparing this with the filenames stored in the load_table.csv file. For each file that is not found it will go ahead and load the logs into the events_summary.json file.

The actual loading of the logs is controlled by the loadjson_func inside the importjson.py file. The logic on how to handle the different calls is available inside this python file. The function loadjson_func returns the number of records loaded for each file which is then inserted into the load_table.csv file alongside the filename.

Assuming that the logs are being pushed into a directory that is sitting in a linux data pipeline server the architecture on the pdf file architecture.pdf will be used. This architecture provides the dataScience team the opportunity to choose a suitable platform they want to access the data from.



Please note they are va