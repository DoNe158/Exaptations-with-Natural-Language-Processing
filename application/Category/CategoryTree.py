import csv
import sys

from application.Scraper import CategoryScraper
from application.Matching import NLPHelper, Calculator
from application.Validator import Validator
from application.Category import Category


class CategoryTree:
    """
    This class represents a tree structure in which categories and their subcategories are stored. The tree is
    based on a list and uses the class Category to initialize the nodes (categories) of the tree.
    Every CategoryTree starts with its root node which is called 'Category' and has '0' as an id.
    This class offers different methods to set up a tree by reading a csv file that represents a category distinction
    according to the taxonomy of the IAB with a maximum level of depth of 4, i.e. 3 subcategories.
    Moreover, methods to find a category by its name or id as well as methods to set the parent-child-relationship
    are implemented within this class.

    - this class has a class variable, that is called "root" and represents a connector for all main categories
    that are listed within the IAB taxonomy.
    """

    root = Category.Category("0", "Category")

    def __init__(self):
        self.root = Category.Category(0, "Category")

    @classmethod
    def get_categories(cls, csv_data) -> list:
        """
        Reads the given csv file and extracts every category. To prevent multiple categories, only the entry at
        index 2 (the name of the category) is considered. Besides the name, the category id as well as the category of
        the parent category is extracted and stored.

        :param csv_data: csv file to be read.
        :return: list of type Category that contains all categories.
        """

        try:
            Validator.check_file_existence(csv_data)
            category_dict_list = cls.convert_csv_into_dict(csv_data)
            category_list = list()
            with open(csv_data, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")
                next(csv_reader)

                for dictionary in category_dict_list:
                    category = Category.Category(dictionary.get("category id"), dictionary.get("category name"))
                    Category.Category.set_parent_id(category, dictionary.get("parent id"))
                    category_list.append(category)

            return category_list

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def get_tier(cls, line_tier):
        """
        Calculates the depth of the category within the given csv file.

        :param line_tier: line that is read from the csv file.
        :return: level of depth for the lowest subcategory in the category tree.
        """

        try:
            Validator.check_empty_string(line_tier)

            if line_tier[4] == "":
                return "1"
            if line_tier[5] == "":
                return "2"
            if line_tier[6] == "":
                return "3"
            if line_tier[6] != "":
                return "4"

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def find_category_by_name(cls, category_list, category_name) -> Category:
        """
        Returns the category with the given name.

        :param category_list: list of type Category that contains all categories.
        :param category_name: name of the category to be searched.
        :return: category with the given name.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_name(category_name)

            for category_1 in category_list:
                if category_1.name == category_name:
                    return category_1
            raise Exception('A category with this name does not exist')

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def find_category_by_id(cls, category_list, id_to_be_searched) -> Category:
        """
        Returns the category with the given id.

        :param category_list: list of type Category that contains all categories.
        :param id_to_be_searched: id to be searched.
        :return: category with the given id.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_id(id_to_be_searched)

            for category in category_list:
                if category.category_id == str(id_to_be_searched):
                    return category
            raise Exception("No category with the given id!")

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_tier(cls, csv_file, category_list):
        """
        Calculates the depth level of each category in the Category Tree that is stored in a list containing all
        categories.

        :param csv_file: csv file with all categories to be read.
        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_file_existence(csv_file)

            with open(csv_file, "r") as csv_data:
                csv_reader = csv.reader(csv_data, delimiter=";")
                next(csv_reader)
                for line in csv_reader:
                    category_name = line[2]
                    category = cls.find_category_by_name(category_list, category_name)
                    tier = cls.get_tier(line)
                    category.set_tier(tier)

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def set_tier_1(cls, category_list, parent_line):
        """
        Sets a main category as a child of the root category 'Category'.
        :param category_list: list of type Category that contains all categories.
        :param parent_line: one line of the csv file.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_string(parent_line)

            child_category = cls.find_category_by_name(category_list, parent_line[2])
            cls.root.children.append(child_category)

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_tier_2_and_above(cls, category_list, parent_line, tier):
        """
        Matches a child with its parent by reading a given line from the csv file. The tier determines the level
        of depth in category tree in which the matching needs to take place.

        :param category_list: list of type Category that contains all categories.
        :param parent_line: one line of the csv file.
        :param tier: level op depth in the category tree.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_string(parent_line)

            category_parent = cls.find_category_by_name(category_list, parent_line[tier + 1])
            child_category = cls.find_category_by_name(category_list, parent_line[tier + 2])
            category_parent.children.append(child_category)

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_child(cls, parent_line, category_list):
        """
        Uses one line of the csv file to match a child with its parent. All dependencies in the given line are
        considered. To do so, the tier of the passed line is considered in order to determine the amount of
        subcategories. In order to set the child, the method 'set_tier_2_and_above()' is used.

        :param parent_line: one line of the csv file.
        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_string(parent_line)

            tier = cls.get_tier(parent_line)

            if tier == "1":
                cls.set_tier_1(category_list, parent_line)

            if tier == "2":
                cls.set_tier_2_and_above(category_list, parent_line, 2)

            if tier == "3":
                cls.set_tier_2_and_above(category_list, parent_line, 2)
                cls.set_tier_2_and_above(category_list, parent_line, 3)

            if tier == "4":
                cls.set_tier_2_and_above(category_list, parent_line, 2)
                cls.set_tier_2_and_above(category_list, parent_line, 3)
                cls.set_tier_2_and_above(category_list, parent_line, 4)

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_children(cls, file, category_list):
        """
        Sets all children according to the given csv file.

        :param file: csv file that contains all information about the categories.
        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_file_existence(file)

            with open(file, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")
                next(csv_reader)

                for line in csv_reader:
                    cls.set_child(line, category_list)

        except (ValueError, FileNotFoundError) as error:
            sys.exit(str(error))

    @classmethod
    def set_all_parents(cls, category_list, csv_data):
        """
        Sets the parents for all categories of the entire csv file.

        :param category_list: list of type Category that contains all categories.
        :param csv_data: csv file that contains all information about the categories.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_file_existence(csv_data)

            with open(csv_data, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=";")
                next(csv_reader)

                for line in csv_reader:
                    if cls.get_tier(line) != "1":
                        cls.set_parent(category_list, line)

        except (ValueError, FileNotFoundError) as error:
            sys.exit(str(error))

    @classmethod
    def set_parent(cls, category_list, line):
        """
        For each entry of the list of categories, the parent of the category will be set. In case of a main node
        (tier = 1), nothing will happen. If the level is deeper (2 - 4), the parent category will be added by using the
        parent id given in the csv file.

        :param category_list: list of type Category that contains all categories.
        :param line: one line of the csv file.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_string(line)

            tier_level = cls.get_tier(line)
            if tier_level == "1":
                child = cls.find_category_by_id(category_list, line[0])
                cls.root.children.append(child)
            if (tier_level == "2") or (tier_level == "3") or (tier_level == "4"):
                parent = cls.find_category_by_id(category_list, line[1])
                child = cls.find_category_by_id(category_list, line[0])
                child.parent = parent

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def print_categories(cls, category_list):
        """
        Prints the entire category list with name, id, parent, id of the parent, and all children (in case the category
        is not a main category).

        param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            print(f"Root category '{cls.root.name}' ({cls.root.category_id}) has no parents and the following children:")
            for child in cls.root.children:
                print(child.name)
            for category in category_list:
                if category.parent == cls.root:
                    print(f"'{category.name}' ({category.category_id}) is a main category and has the following children:")
                if category.parent is not None:
                    if not category.children:
                        print(
                            f"'{category.name}' ({category.category_id}) has the parent category '{category.parent.name}' "
                            f"({category.parent.category_id}) and no children.")
                    else:
                        print(
                            f"'{category.name}' ({category.category_id}) has the parent category '{category.parent.name}' "
                            f"({category.parent.category_id}) and the following children:")
                        for child in category.children:
                            if child == category.children[-1]:
                                print(child.name)
                            else:
                                print(child.name, end=" - ")

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_up_tree(cls, csv_data) -> list:
        """
        Uses the csv file and methods of the class CategoryTree in order to set up the entire category tree.

        :param csv_data: csv file that contains all categories.
        """

        try:
            Validator.check_file_existence(csv_data)

            category_list = cls.get_categories(csv_data)
            category_list.insert(0, cls.root)
            cls.set_children(csv_data, category_list)
            cls.delete_duplicates(category_list)
            cls.set_all_parents(category_list, csv_data)
            cls.set_tier(csv_data, category_list)
            cls.set_structure_id(category_list)
            cls.initialize_root(category_list)
            cls.set_root_as_parent(category_list)
            cls.concatenate_structure_id(category_list)

            return category_list

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def set_structure_id(cls, category_list):
        """
        Calculates and sets the structure id of each category. Each tier is represented by two digits. In case there
        are leading zeros, the category is represented by only one digit which will be adapted in the
        function "concatenate_structure_id".

        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            tmp_structure_id = 1

            for category in category_list:
                if category.tier == "1":
                    category.set_structure_id(tmp_structure_id)
                    tmp_structure_id = tmp_structure_id + 1
            tmp_structure_id = 1

            for category in category_list:
                if category.tier == "1":
                    for child_category in category.children:
                        child_category.structure_id = tmp_structure_id
                        tmp_structure_id = tmp_structure_id + 1
                    tmp_structure_id = 1

            for category in category_list:
                if category.tier == "2":
                    for child_category in category.children:
                        child_category.structure_id = tmp_structure_id
                        tmp_structure_id = tmp_structure_id + 1
                    tmp_structure_id = 1

            for category in category_list:
                if category.tier == "3":
                    for child_category in category.children:
                        child_category.structure_id = tmp_structure_id
                        tmp_structure_id = tmp_structure_id + 1
                    tmp_structure_id = 1

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def concatenate_structure_id(cls, category_list):
        """
        Generates the structure id for every category by concatenating the specific structure ids of the parent
        categories. After that, every category has its unique structure id that represents its position in the
        category tree hierarchy. The structure id is set to every category.

        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            for category in category_list:
                if category.tier == "4":
                    category.structure_id = str(category.parent.parent.parent.structure_id).zfill(2) + \
                                            str(category.parent.parent.structure_id).zfill(2) + \
                                            str(category.parent.structure_id).zfill(2) + str(category.structure_id).zfill(2)

            for category in category_list:
                if category.tier == "3":
                    category.structure_id = str(category.parent.parent.structure_id).zfill(2) + \
                                            str(category.parent.structure_id).zfill(2) + \
                                            str(category.structure_id).zfill(2) + "00"

            for category in category_list:
                if category.tier == "2":
                    category.structure_id = str(category.parent.structure_id).zfill(2) + \
                                            str(category.structure_id).zfill(2) + "0000"

            for category in category_list:
                if category.tier == "1":
                    category.structure_id = str(category.structure_id).zfill(2) + "000000"

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def set_root_as_parent(cls, category_list):
        """
        Sets the parent (root) for every main category (tier 1).

        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            for category in category_list:
                if category.tier == "1":
                    category.parent = cls.root

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def initialize_root(cls, category_list):
        """
        Set the root category as the parent of all main categories (tier = 1).

        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            cls.root.tier = "0"
            for category in category_list:
                if cls.get_tier == "1":
                    category_tier_1 = category
                    cls.root.children.append(category)
                    category_tier_1.parent = cls.root

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def delete_duplicates(cls, category_list):
        """
        Deletes the duplicates in the children list of all categories since they are counted every single time
        when they occur in the csv file.

        :param category_list: list of type Category that contains all categories.
        """

        try:
            Validator.check_empty_list(category_list)

            for category in category_list:
                list_no_duplicates = []
                for child in category.children:
                    if child not in list_no_duplicates:
                        list_no_duplicates.append(child)
                category.children = list_no_duplicates

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def convert_csv_into_dict(cls, csv_file) -> list:
        """
        Converts the given csv file into a list containing dictionaries for each category.
        The keys are identical to the first line of the csv file whereas the values are represented
        by the content of each line.

        :param csv_file: csv file to be read.
        :return: list of dictionaries containing each categories with the given keys and values.
        """

        try:
            Validator.check_file_existence(csv_file)

            category_id = "category id"
            parent_id = "parent id"
            category_name = "category name"
            tier_1 = "tier 1"
            tier_2 = "tier 2"
            tier_3 = "tier 3"
            tier_4 = "tier 4"

            category_list = []

            with open(csv_file, "r") as csv_data:
                csv_reader = csv.reader(csv_data, delimiter=";")
                next(csv_reader)

                for line in csv_reader:
                    category_dict = {category_id: line[0], parent_id: line[1], category_name: line[2], tier_1: line[3],
                                     tier_2: line[4], tier_3: line[5], tier_4: line[6]}
                    category_list.append(category_dict)

            return category_list

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def create_category_profile(cls, application_name, category_list, language, additional_stopwords=None):
        """
        Scrapes the description of a given name of an smartphone application and matches it to the most fitting category
        within the category tree.

        :param application_name: name of a specific application that is used to compare with the user's description.
        :param category_list: list of type Category that contains all categories.
        :param language: language of the description.
        :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
        defined in the nltk package.
        :return: best matching category within the category tree for the given application.
        """

        try:
            Validator.check_empty_list(category_list)
            Validator.check_empty_string(application_name)
            Validator.check_language(language)

            success = False

            while success is False:
                try:
                    CategoryScraper.get_application_description(application_name)
                    success = True
                except:
                    pass

            keyword_dict = NLPHelper.generate_keyword_dict_from_user_description("./files/category_description.txt", language,
                                                                                 additional_stopwords)

            best_matches = Calculator.get_top10_best_matches_application(category_list, keyword_dict)
            # best_match = Calculator.calculate_best_matching_category_initial(category_list, keyword_dict)

            if best_matches:
                matches_dict = Calculator.calculate_main_category_application_matching_values(best_matches, category_list)
                top_match = Calculator.calculate_highest_matching_value(matches_dict)
                return top_match
            else:
                return best_matches

        except ValueError as error:
            sys.exit(str(error))
