"""
Loading output of sql querries to CSV
"""

import os

import pandas as pd


def add_slash(dir_name):
    """
    Adds a slash at the end of a string if not present
    """
    if not dir_name.endswith('/'):
        dir_name += '/'
    return dir_name


def make_dir(filepath):
    """
    Creates a directory from a file path if the directory does not exist
    """
    file_dir = os.path.dirname(filepath)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


def read_sql_data(filepath, connection):
    """
    Load output of sql file into  a data frame
    """
    # tech debt: check if sql file
    # Read the sql file
    opened_query = open(filepath, 'r')
    print('Read ' + filepath)
    # connection
    data_frame = pd.read_sql_query(opened_query.read(), connection)
    print('Stored output of ' + filepath + ' into data frame')
    return data_frame


def sql_to_csv(filepath, connection, output_folder='output/'):
    """
    Writes output of a single sql query to CSV
    """
    data_frame = read_sql_data(filepath, connection)
    # add slash if needed
    output_folder = add_slash(dir_name=output_folder)
    output_filepath = output_folder + filepath.split('.')[0] + '.csv'
    # create director if needed
    make_dir(output_filepath)
    # write to output folder
    data_frame.to_csv(output_filepath, sep='\t', encoding='utf-8')
    print('Wrote output to ' + output_filepath)


def sqls_to_csv(filepath, connection, output_folder='output/'):
    """
    Writes output of sql queries to a CSV files
    """
    if os.path.isdir(filepath):
        file_list = os.listdir(filepath)
        filepath = add_slash(dir_name=filepath)
        for file in file_list:
            if file.endswith(".sql"):
                file = filepath + file
                sql_to_csv(filepath=file, connection=connection,
                           output_folder=output_folder)
    else:
        sql_to_csv(filepath=filepath, connection=connection,
                   output_folder=output_folder)
