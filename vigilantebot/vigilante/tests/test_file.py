import json
import os

import pytest
from os.path import isfile

from vigilante import fileutils


@pytest.fixture
def file():
    return 'test_file.json'


@pytest.fixture
def key():
    return 'test_key'


@pytest.fixture
def key_content():
    return {'a_key': 'a_value'}


def delete_file(file):
    os.remove(file)


def test_create_file(file):
    fileutils.create_empty_json_file(file)
    assert isfile(file)
    delete_file(file)


def test_create_file_is_json_valid(file):
    fileutils.create_empty_json_file(file)
    with open(file, 'r') as f:
        data = json.load(f)

    assert data == {}
    delete_file(file)


def test_create_empty_key_in_file(file, key):
    fileutils.create_empty_json_file(file)
    fileutils.create_empty_key_in_file(file, key)
    with open(file, 'r') as f:
        data = json.load(f)

    assert key in data
    delete_file(file)


def test_update_file_key(file, key, key_content):
    fileutils.create_empty_json_file(file)
    fileutils.create_empty_key_in_file(file, key)
    fileutils.update_file_key(file, key, key_content, 'child_key')
    with open(file, 'r') as f:
        data = json.load(f)

    assert data[key]['child_key'] == key_content
    delete_file(file)


def test_get_file_key_content(file, key, key_content):
    fileutils.create_empty_json_file(file)
    fileutils.create_empty_key_in_file(file, key)
    fileutils.update_file_key(file, key, key_content, 'child_key')
    data = fileutils.get_file_key_content(file, key, 'child_key')
    # with open(file, 'r') as f:
    #     data = json.load(f)

    assert data == key_content
    delete_file(file)
