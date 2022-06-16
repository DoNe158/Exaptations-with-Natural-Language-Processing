import os


def check_empty_string(line):
    if not line:
        raise ValueError('Error: The given string is empty.')


def check_empty_id(category_id):
    if category_id == "":
        raise ValueError('Error: This id is empty.')


def check_empty_name(name):
    if name == "":
        raise ValueError('Error: This name is empty.')


def check_empty_list(category_list):
    if not category_list:
        raise ValueError('Error: No categories are stored.')


def check_file_existence(file):
    if not os.path.isfile(file):
        raise FileNotFoundError('Error: This file does not exist.')


def check_language(language):
    if language != 'english':
        raise ValueError('Error: English must be set as language.')


def check_existence_category(category):
    if category is None:
        raise ValueError('Error: Category was not found.')
