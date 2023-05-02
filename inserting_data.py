from import_data.insert_data import *
import os

# get the current working directory
current_dir = os.getcwd()

# check if the data folder exists in the current directory
path = os.path.join(current_dir, 'data')

file = 'bagel twists.txt'
filename = os.path.join(path, file)

remove_new_line(filename)
add_new_line(filename)
insert_to_db(filename, "Food-RS-0")
