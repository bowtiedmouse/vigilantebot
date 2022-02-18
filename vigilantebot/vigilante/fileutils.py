import os
import json
import logging

logger = logging.getLogger(__name__)


def create_empty_json_file(file: str):
    with open(file, "w") as f:
        json.dump({}, f)


def create_empty_key_in_file(file: str, key: str):
    if not os.path.isfile(file) or os.stat(file).st_size == 0:
        create_empty_json_file(file)

    update_file_key(file, key, {})


def update_file_key(file: str, primary_key: str, content, secondary_key: str = ""):
    try:
        with open(file, "r") as f:
            file_data = json.load(f)

        if primary_key not in file_data:
            file_data[primary_key] = {}

        if not secondary_key:
            file_data[primary_key] = content
        else:
            file_data[primary_key][secondary_key] = content

        # The default umask is 0o22 which turns off write permission of group and others
        os.umask(0)
        with open(os.open(file, os.O_CREAT | os.O_WRONLY, 0o777), "w") as f:
            json.dump(file_data, f, indent=2)

    except FileNotFoundError:
        logger.warning(f"File not found: {file}. Couldn't update it.")
        raise


def get_file_key_content(file: str, primary_key: str, secondary_key: str = ""):
    key_content = {}

    try:
        key_content = _get_key_content(file, primary_key, secondary_key)
    except FileNotFoundError:
        logger.info(f"File not found: {file}. Creating it...")
        create_empty_json_file(file)
    except json.decoder.JSONDecodeError:
        logger.warning("File is empty or malformed. Will be restored.")
        create_empty_json_file(file)

    return key_content


def get_file_dict(file: str) -> dict:
    file_dict = {}
    try:
        with open(file, "r") as f:
            file_dict = json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {file}.")
    except json.decoder.JSONDecodeError:
        logger.warning("File is empty or malformed.")

    return file_dict


def update_file(file: str, content: dict) -> None:
    try:
        os.umask(0)
        with open(os.open(file, os.O_CREAT | os.O_WRONLY, 0o777), "w") as f:
            json.dump(content, f, indent=2)
    except FileNotFoundError:
        logger.warning(f"File not found: {file}.")


def _get_key_content(file: str, primary_key: str, secondary_key: str):
    with open(file, "r") as f:
        saved_data = json.load(f)

        try:
            key_content = saved_data[primary_key]
            if secondary_key:
                key_content = key_content[secondary_key]
            return key_content
        except KeyError:
            if primary_key not in saved_data:
                logger.warning(f"{primary_key} not found in {file}.")
            return {}
