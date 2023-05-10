from import_data.insert_data import *
import os

if __name__ == '__main__':
    # get the current working directory
    current_dir = os.getcwd()

    # check if the data folder exists in the current directory
    path = os.path.join(current_dir, 'data')

    file = 'angelica sinensis'
    filename = os.path.join(path, file + ".txt")

    remove_new_line(filename)
    add_new_line(filename)
    insert_to_db(filename, "Food-RS-0", "quantity", "10000")
