import json

def read_data_from_json(file_name):
    """Read data from json file.

    :file_name: name of the json file
    :return: dictionary read from the json file
    """
    try:
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        return data
    except FileNotFoundError:
        print("No such file: " + file_name)
        exit()