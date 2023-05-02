from import_data.insert_data import *
import os

path = 'c:\\Users\\Dell\\Downloads\\mfp\\data'
file = 'tempura flour.txt'
filename = os.path.join(path, file)

# remove_new_line(filename)
# add_new_line(filename)
insert_to_db(filename)
