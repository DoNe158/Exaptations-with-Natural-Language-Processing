import sys
import play_scraper
import json
import re

from application.Matching import NLPHelper
from application.Validator import Validator


def get_application_description(application_name):
    """
    Fetches the description text for the given application by using the Google Play Scraper. The results are stored
    to "./files/category_description.txt"

    :param application_name: name of the application that is searched.
    :return: description of the given application from the Play Store.
    """

    try:
        Validator.check_empty_string(application_name)

        matches = play_scraper.search(application_name)
        app_id = ''

        for element in matches:
            if element['title'] == application_name:
                app_id = element['app_id']
                break

        if app_id == '':
            raise ValueError('Error: The app was not found. Please check whether you entered the full and correct name '
                             'of the application.')

        application = play_scraper.details(app_id)
        description = application['description']

        description = NLPHelper.clean_file(description)

        with open("./files/category_description.txt", "w", encoding="utf-8") as file:
            file.write(description)

    except ValueError as error:
        sys.exit(str(error))


def store_all_descriptions(category_list) -> dict:
    """
    Scrapes all descriptions for every category in the given category list and stores the result in a dictionary.

    :param category_list: list of type Category that contains all categories.
    :return: dictionary containing all names and the descriptions for each category.
    """

    try:
        Validator.check_empty_list(category_list)

        category_dict = dict()
        for category in category_list:
            if category.name == 'Category':
                pass
            else:
                success = False
                while success is False:
                    try:
                        dict_key = category.name
                        dict_value = ""
                        dict_value_tmp = play_scraper.search(category.name, detailed=True)
                        for item in dict_value_tmp:
                            for key, value in item.items():
                                if key == "description":
                                    value = clean_description_file(value)
                                    dict_value = dict_value + value
                        category_dict[dict_key] = dict_value
                        write_dict_to_file(category_dict, "./files/dict.json")

                        success = True
                        print(category.name + ": successful")
                    except:
                        pass

        return category_dict

    except ValueError as error:
        sys.exit(str(error))


def clean_description_file(description) -> str:
    """
    Cleans the description of a category that is scraped via the Category CategoryScraper. All links to websites, email
    addresses and special characters are removed. All non-ASCII characters are removed from the description.

    :param description: description of a category that is scraped by the category scraper.
    """

    try:
        Validator.check_empty_string(description)

        text_cleaned = re.sub(r"http\S+", "", description)
        text_cleaned = re.sub(r"www\S+", "", text_cleaned)
        text_cleaned = re.sub(r"\S*@\S*\s?", "", text_cleaned)
        text_cleaned = re.sub(r'[-.?!,:;()|0-9+&"/%$*=]', ' ', text_cleaned)
        text_cleaned = text_cleaned.encode("ascii", "ignore")
        text_cleaned = text_cleaned.lower()
        text_cleaned = text_cleaned.decode('utf-8')

        return text_cleaned

    except ValueError as error:
        sys.exit(str(error))


def write_dict_to_file(category_dict, file):
    """
    Writes a dictionary to a json file.

    :param category_dict: dictionary containing name and descriptions of categories.
    :param file: json file where the dictionary is written to.
    """

    try:
        Validator.check_file_existence(file)

        with open(file, "w") as output_file:
            json.dump(category_dict, output_file)

    except FileNotFoundError as error:
        sys.exit(str(error))
