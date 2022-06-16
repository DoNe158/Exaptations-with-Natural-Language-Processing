import sys
from itertools import islice

from application.Category import Category
from application.Category.CategoryTree import CategoryTree
from application.Matching import NLPHelper
from application.Matching.NLPHelper import initialize_keywords_from_keywords_dict
from application.Scraper import CategoryScraper
from application.Validator import Validator


def get_total_occurrences(keywords_dict) -> int:
    """
    Calculates the total amount of occurrences of the top keywords that are stored with a category.

    :param keywords_dict: dictionary containing keywords with their occurrences.
    :return: total amount of occurrences.
    """

    total = 0
    for element in keywords_dict:
        total = total + keywords_dict[element]

    return total


def calculate_normalized_values_of_keywords(keywords_dict) -> dict:
    """
    Calculates normalized values of each value in the given dictionary by dividing the number of occurrences of each
    keyword by the total amount of occurrences of keywords in the given dictionary.

    :param keywords_dict: dictionary containing keywords with their occurrences.
    :return: dictionary containing normalized values of the given dictionary.
    """

    normalized_values_dict = dict()
    total = get_total_occurrences(keywords_dict)

    for element in keywords_dict:
        normalized_values_dict[element] = keywords_dict[element] / total

    return normalized_values_dict


def calculate_matching_values(normalized_keywords_dict, normalized_user_dict) -> float:
    """
    Calculates the matching values for the keywords of both the category and the user's description. To do so,
    normalized values of the keywords / occurrences of the keywords are necessary.

    :param normalized_keywords_dict: dictionary containing normalized values of the keywords of the category.
    :param normalized_user_dict: dictionary containing normalized values of the keywords extracted from the
    user's description.
    :return: matching value of both dictionaries.
    """

    result = 0
    for element in normalized_user_dict:
        if element in normalized_keywords_dict:
            result = result + normalized_user_dict[element] * normalized_keywords_dict[element]

    return round(result, 4)


def calculate_matching_values_all_categories(category_list, user_dict) -> dict:
    """
    Calculates matching values of all categories and the given user description. The user's description needs to be
    stored as a dictionary containing the name of the token and its number of occurrences in the description. The
    dictionary will be normalized within this function.

    :param category_list: list of type Category that contains all categories.
    :param user_dict: dictionary containing all tokens with their number of occurrences in the description of the user.
    :return: dictionary holding matching values with every category in the category list.
    """

    try:
        Validator.check_empty_list(category_list)

        matching_values_dict = dict()
        user_dict_normalized = calculate_normalized_values_of_keywords(user_dict)

        for category in category_list:
            normalized_keywords_dict = calculate_normalized_values_of_keywords(category.keywords)
            result = calculate_matching_values(
                calculate_normalized_values_of_keywords(normalized_keywords_dict), user_dict_normalized)
            matching_values_dict[category.name] = result

        return matching_values_dict

    except ValueError as error:
        sys.exit(str(error))


def calculate_best_matching_category(category_list, user_dict):
    """
    Calculates the best matching category for the given user's description.

    :param category_list: list of type Category that contains all categories.
    :param user_dict: dictionary containing all tokens with their number of occurrences in the description of the user.
    :return: dictionary holding the best match with the user's description.
    """

    try:
        Validator.check_empty_list(category_list)

        best_match = dict()
        best_matching_category_name = ""
        best_matching_category_occurrences = 0
        matching_values_dict = calculate_matching_values_all_categories(category_list, user_dict)

        for element in matching_values_dict:
            if matching_values_dict[element] > best_matching_category_occurrences:
                best_matching_category_occurrences = matching_values_dict[element]
                best_matching_category_name = element

        if best_matching_category_occurrences >= 0.01:

            best_match[best_matching_category_name] = best_matching_category_occurrences

            best_matching_category = best_matching_category_name
            category_comparison = CategoryTree.find_category_by_name(category_list, best_matching_category)
            return category_comparison

        else:
            return -1

    except ValueError as error:
        sys.exit(str(error))


def calculate_best_matching_category_initial(category_list, user_dict):
    """
    Calculates the best matching category for the given user's description.

    :param category_list: list of type Category that contains all categories.
    :param user_dict: dictionary containing all tokens with their number of occurrences in the description of the user.
    :return: dictionary holding the best match with the user's description.
    """

    try:
        Validator.check_empty_list(category_list)

        best_match = dict()
        best_matching_category_name = ""
        best_matching_category_occurrences = 0
        matching_values_dict = calculate_matching_values_all_categories(category_list, user_dict)

        for element in matching_values_dict:
            if matching_values_dict[element] > best_matching_category_occurrences:
                best_matching_category_occurrences = matching_values_dict[element]
                best_matching_category_name = element

        best_match[best_matching_category_name] = best_matching_category_occurrences

        best_matching_category = best_matching_category_name
        category_comparison = CategoryTree.find_category_by_name(category_list, best_matching_category)
        return category_comparison

    except ValueError as error:
        sys.exit(str(error))


def take(number, iterable):
    """
    Return the first n (number) items of the iterable as a list.

    :param number: number of entries from the iterable .
    :param iterable: iterable data type.
    :return: list containing the first n (number) entries of the given iterable.
    """

    return list(islice(iterable, number))


def get_top10_best_matches(category_list, user_dict):
    """
    Returns the 10 best fitting categories for the user's description.

    :param category_list: list of type Category that contains all categories.
    :param user_dict: dictionary containing all tokens with their number of occurrences in the description of the user.
    :return: Top 10 categories that matches the best with the user's description.
    """

    try:
        Validator.check_empty_list(category_list)

        matching_values_dict = calculate_matching_values_all_categories(category_list, user_dict)
        tmp_dict = \
            {key: value for key, value in sorted(matching_values_dict.items(), key=lambda item: item[1], reverse=True)}

        top_ten_list = take(10, tmp_dict.items())
        list_tmp = list()

        for element in top_ten_list:
            if element[1] >= 0.01:
                list_tmp.append(element)

        top_ten_dict = dict(list_tmp)

        return top_ten_dict

    except ValueError as error:
        sys.exit(str(error))


def get_top10_best_matches_application(category_list, user_dict) -> dict:
    """
    Returns the 10 best fitting categories for the user's description.

    :param category_list: list of type Category that contains all categories.
    :param user_dict: dictionary containing all tokens with their number of occurrences in the description of the user.
    :return: Top 10 categories that matches the best with the user's description.
    """

    try:
        Validator.check_empty_list(category_list)

        matching_values_dict = calculate_matching_values_all_categories(category_list, user_dict)
        tmp_dict = \
            {key: value for key, value in sorted(matching_values_dict.items(), key=lambda item: item[1], reverse=True)}

        top_ten_list = take(10, tmp_dict.items())
        list_tmp = list()

        for element in top_ten_list:
            if element[1] >= 0.008:
                list_tmp.append(element)
            list_tmp.append(element)

        top_ten_dict = dict(list_tmp)

        return top_ten_dict

    except ValueError as error:
        sys.exit(str(error))


def calculate_highest_matching_value(matching_dict):
    tmp_dict = \
        {key: value for key, value in sorted(matching_dict.items(), key=lambda item: item[1], reverse=True)}
    top_match = take(1, tmp_dict.items())

    top_match = dict(top_match)

    return top_match


def check_distances(structure_id_1):
    """
    Checks whether the structure id of a category corresponds with the syntactical rules of the category tree.
    A category cannot be a subcategory without a parent category, e.g. 10200030 is not possible, since at index 4 and 5,
    there are two zeros which means that no parent category is given. Every two digits represent a category in the
    hierarchy, whereas the first two digits refer to a main category on the most upper level (tier 1).

    :param structure_id_1: structure id of a category.
    """

    if structure_id_1[0] == "0" and structure_id_1[1] == "0":
        raise Exception("Incorrect structure id!")
    if (structure_id_1[2] == "0" and structure_id_1[3] == "0"
            and ((structure_id_1[4] == "0" and structure_id_1[5] != "0")
                 or (structure_id_1[4] != "0" and structure_id_1[5] == "0")
                 or (structure_id_1[6] == "0" and structure_id_1[7] != "0")
                 or (structure_id_1[6] != "0" and structure_id_1[7] == "0"))):
        raise Exception("Incorrect structure id!")

    if (structure_id_1[4] == "0" and structure_id_1[5] == "0"
            and ((structure_id_1[6] == "0" and structure_id_1[7] != "0") or (
                    structure_id_1[6] != "0" and structure_id_1[7] == "0"))):
        raise Exception("Incorrect structure id!")


def calculate_distance(structure_id_1, structure_id_2):
    """
    Calculates the distance of two categories. To do so, the structure id of each category is considered. The distance
    between two main categories (on tier 1) is calculated with a distance of 1 for each side of the tree. The total
    distance would therefore be 2. For every branch downwards the half of the distance is considered, i.e. 0.5
    on subcategories of the main categories (tier 2). Supposed there are two subcategories of two different main
    categories, the distance is calculated as 0.5 for the distance between subcategory to main category, 1 for the
    distance between the main category and the root which results in 1.5 for half the way. Since the other distance
    is at the same level, the distance is doubled. This results in 3. The distance on tier 3 is 0.25,
    and for tier 4 0.125.

    :param structure_id_1: structure id (string with a length of 8) of the first category.
    :param structure_id_2: structure id (string with a length of 8) of the second category.
    :return: distance between two categories.
    """
    check_distances(structure_id_1)
    check_distances(structure_id_2)

    distance = 0
    if structure_id_1 != structure_id_2:
        if structure_id_1[0] != structure_id_2[0] or structure_id_1[1] != structure_id_2[1]:
            if ((structure_id_1[0] == "0" and structure_id_1[1] == "0")
                and not (structure_id_2[0] == "0" and structure_id_2[1] == "0")) \
                    or ((structure_id_2[0] == "0" and structure_id_2[1] == "0")
                        and not (structure_id_1[0] == "0" and structure_id_1[1] == "0")):
                distance = distance + 2
            else:
                distance = distance + 2 * 2

        if (structure_id_1[2] != structure_id_2[2] or structure_id_1[3] != structure_id_2[3]) \
                or ((structure_id_1[2] == structure_id_2[2] and structure_id_1[3] == structure_id_2[3])
                    and (structure_id_1[0] != structure_id_2[0] or structure_id_1[1] != structure_id_2[1])):
            if ((structure_id_1[2] == "0" and structure_id_1[3] == "0") and not (
                    structure_id_2[2] == "0" and structure_id_2[3] == "0")) \
                    or ((structure_id_2[2] == "0" and structure_id_2[3] == "0") and not (
                    structure_id_1[2] == "0" and structure_id_1[3] == "0")):
                distance = distance + 0.5
            else:
                distance = distance + 0.5 * 2

        if (structure_id_1[4] != structure_id_2[4] or structure_id_1[5] != structure_id_2[5]) \
                or ((structure_id_1[4] == structure_id_2[4] and structure_id_1[5] == structure_id_2[5])
                    and (structure_id_1[2] != structure_id_2[2] or structure_id_1[3] != structure_id_2[3])) \
                or ((structure_id_1[4] == structure_id_2[4] and structure_id_1[5] == structure_id_2[5])
                    and (structure_id_1[2] == structure_id_2[2] and structure_id_1[3] == structure_id_2[3])
                    and (structure_id_1[0] != structure_id_2[0] or structure_id_1[1] != structure_id_2[1])):
            if ((structure_id_1[4] == "0" and structure_id_1[5] == "0") and not (
                    structure_id_2[4] == "0" and structure_id_2[5] == "0")) \
                    or ((structure_id_2[4] == "0" and structure_id_2[5] == "0") and not (
                    structure_id_1[4] == "0" and structure_id_1[5] == "0")):
                distance = distance + 0.25
            else:
                distance = distance + 0.25 * 2

        if (structure_id_1[6] != structure_id_2[6] or structure_id_1[7] != structure_id_2[7]) \
                or ((structure_id_1[6] == structure_id_2[6] and structure_id_1[7] == structure_id_2[7])
                    and (structure_id_1[4] != structure_id_2[4] or structure_id_1[5] != structure_id_2[5])) \
                or ((structure_id_1[6] == structure_id_2[6] and structure_id_1[7] == structure_id_2[7])
                    and (structure_id_1[4] == structure_id_2[4] and structure_id_1[5] == structure_id_2[5])
                    and (structure_id_1[2] != structure_id_2[2] or structure_id_1[3] != structure_id_2[3])) \
                or ((structure_id_1[6] == structure_id_2[6] and structure_id_1[7] == structure_id_2[7])
                    and (structure_id_1[4] == structure_id_2[4] and structure_id_1[5] == structure_id_2[5])
                    and (structure_id_1[2] == structure_id_2[2] or structure_id_1[3] == structure_id_2[3])
                    and structure_id_1[0] != structure_id_2[0] or structure_id_1[1] != structure_id_2[1]):
            if ((structure_id_1[6] == "0" and structure_id_1[7] == "0") and not (
                    structure_id_2[6] == "0" and structure_id_2[7] == "0")) \
                    or ((structure_id_2[6] == "0" and structure_id_2[7] == "0") and not (
                    structure_id_1[6] == "0" and structure_id_1[7] == "0")):
                distance = distance + 0.125
            else:
                distance = distance + 0.125 * 2

    return distance


def get_matches_application_with_categories(csv_data, language, additional_stopwords, keywords_file, applications):
    """
    Stores all matching values of all applications that are listed in the provided file.

    :param csv_data: csv file to be read.
    :param language: language of the description in the file.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    :param keywords_file: json file containing the keywords for each category.
    :param applications: file containing all applications.
    """

    try:
        Validator.check_file_existence(csv_data)
        Validator.check_language(language)
        Validator.check_file_existence(applications)

        category_list = CategoryTree.set_up_tree(csv_data)
        stopwords_add = NLPHelper.read_additional_stopwords_from_file(additional_stopwords)
        initialize_keywords_from_keywords_dict(category_list, keywords_file)

        with open(applications, 'r', encoding='utf-8') as file:

            for line in file:
                application_name = line
                application_name = application_name.replace('\n','')
                CategoryScraper.get_application_description(application_name)
                keywords_dictionary = NLPHelper.generate_keyword_dict_from_user_description('files/category_description.txt',
                                                                                    language, stopwords_add)
                top10_dict = get_top10_best_matches_application(category_list, keywords_dictionary)

                with open('files/application_matches.txt', "a", encoding='utf-8') as app_file:
                    string_to_write = application_name + ": " + str(top10_dict) + '\n'
                    app_file.write(string_to_write)

    except (ValueError, FileNotFoundError) as error:
        sys.exit(str(error))


# new function since version 2
def calculate_main_category(category) -> Category:
    """
    Calculates the presumed main category for this application.

    :param category: one specific category of the category tree.
    :return: main category of a (sub)category.
    """

    try:
        Validator.check_existence_category(category)

        tier = Category.Category.get_tier(category)
        category_tmp = category
        exit_function = False

        while exit_function is False:
            if tier != "1":
                category_tmp = category_tmp.get_parent()
                tier = category_tmp.get_tier()
            else:
                return category_tmp

    except ValueError as error:
        sys.exit(str(error))


# new function since version 2
def calculate_main_category_application_absolute_number(matching_dict, category_list) -> dict:
    """
    dictionary containing all matching main categories for an application with their absolute number of
    occurrences.

    :param matching_dict: dictionary containing all matching categories for an application.
    :param category_list: list of type Category that contains all categories.
    :return: dictionary containing all matching main categories for an application.
    """

    try:
        Validator.check_empty_list(category_list)

        result_dict = dict()
        already_exists = False

        for key in matching_dict.keys():
            category_tmp = CategoryTree.find_category_by_name(category_list, key)
            parent_category = calculate_main_category(category_tmp)

            for result_key in result_dict.keys():
                if result_key == parent_category.name:
                    already_exists = True
                    result_dict[result_key] = result_dict[result_key] + 1
                    break

            if already_exists is False:
                result_dict[parent_category.name] = 1

        return result_dict

    except ValueError as error:
        sys.exit(str(error))


# new function since version 2
def calculate_main_category_application_matching_values(matching_dict, category_list) -> dict:
    """
    Calculates the main categories of the given dictionary containing all matching categories for a specific
    application.

    :param matching_dict: dictionary containing all matching categories for an application.
    :param category_list: list of type Category that contains all categories.
    :return: dictionary containing all matching main categories for an application with their summarized matching values.
    """

    try:
        Validator.check_empty_list(category_list)

        result_dict = dict()
        already_exists = False

        for key, value in matching_dict.items():
            category_tmp = CategoryTree.find_category_by_name(category_list, key)
            if category_tmp.name != "Category":
                parent_category = calculate_main_category(category_tmp)

                for result_key in result_dict.keys():
                    if result_key == parent_category.name:
                        already_exists = True
                        result_dict[result_key] = result_dict[result_key] + matching_dict[key]
                        break

                if already_exists is False:
                    result_dict[parent_category.name] = matching_dict[key]

        return result_dict

    except ValueError as error:
        sys.exit(str(error))
