from import_data.insert_data import *
import os

import os

def get_most_recent_file(directory):
    files = os.listdir(directory)

    if files:
        most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
        recent_file_path = os.path.join(path, most_recent_file)

        return recent_file_path
    else:
        return None


if __name__ == '__main__':
    # get the current working directory
    current_dir = os.getcwd()

    # check if the data folder exists in the current directory
    path = os.path.join(current_dir, 'data')

    # get the latest file from data directory
    file = get_most_recent_file('E:\\1_RS\\scraping-data\\data')
    
    remove_new_line(file)
    add_new_line(file)
    insert_to_db(file, "NineHealth_2", "quantity", "10000")
