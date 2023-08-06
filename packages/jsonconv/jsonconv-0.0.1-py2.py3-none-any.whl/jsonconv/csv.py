import csv

from . import common


def read(file_path, delimiter=",", **kwargs):
    """Converts CSV file to JSON

    Args:
        file_path (str,path_like): path to the CSV file
        delmiter (str): column delimiter

    Returns:
        json_data (JSON object): data as JSON object
    """
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        json_data = [row for row in reader]
    return json_data


def write(file_path, json_data, delimiter=","):
    """Writes JSON Data to CSV file

    Args:
        file_path (str,path_like): path to the CSV file
        json_data (JSON Object): JSON data to be written
        delmiter (str): column delimiter
    """
    with open(file_path, 'w') as csvfile:
        if isinstance(json_data, dict):  # if only contains one row
            # put in a list for compatiblity with rest of function
            json_data = [json_data]
        columns = common._get_columns(json_data)
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(json_data)
