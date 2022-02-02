import os
import json


def create_empty_json_file(file: str):
    with open(file, "w") as f:
        json.dump({}, f)


def create_empty_key_in_file(file: str, key: str):
    if not os.path.isfile(file) or os.stat(file).st_size == 0:
        create_empty_json_file(file)

    with open(file, "r") as f:
        data = json.load(f)
    if key not in data:
        data[key] = {}
    with open(file, "w") as f:
        json.dump(data, f)


def update_file_key(file: str, primary_key: str, secondary_key: str, content):
    try:
        with open(file, "r") as f:
            file_data = json.load(f)

        if primary_key not in file_data:
            file_data[primary_key] = {}

        file_data[primary_key][secondary_key] = content

        with open(file, "w") as f:
            json.dump(file_data, f)

    except FileNotFoundError:
        print(f"File not found: {file}. Couldn't update it.")
        raise


def get_file_key_content(file: str, primary_key: str, secondary_key: str = "") -> dict:
    key_content = {}

    try:
        with open(file, "r") as f:
            saved_data = json.load(f)
            key_content = saved_data[primary_key]
            if secondary_key:
                key_content = key_content[secondary_key]
    except FileNotFoundError:
        print(f"File not found: {file}. Creating it...")
        create_empty_json_file(file)
    except KeyError:
        print(f"Not found saved record for {primary_key}. Creating an empty one.")
        create_empty_key_in_file(file, primary_key)
    except json.decoder.JSONDecodeError:
        print("File is empty or malformed.")

    return key_content
