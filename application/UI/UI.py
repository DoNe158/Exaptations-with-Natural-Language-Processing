import csv
import sys
import nltk

from application.Scraper import CategoryScraper
from application.Matching import NLPHelper, Calculator
from application.Validator import Validator
from application.Category.CategoryTree import CategoryTree


class UserInterface:

    @classmethod
    def start_application(cls):
        try:
            print("Please indicate the path of the csv file containing the categories")
            path_input = input()
            Validator.check_file_existence(path_input)

            print("Please indicate the language you use (needs to be 'english' right now)")
            language_input = input()
            Validator.check_language(language_input)

            print("Please indicate the path of the file with the additional stopwords.")
            stopwords_input = input()
            Validator.check_file_existence(stopwords_input)

            cls.__print_question_main()
            user_input = input()

            exit_function = False

            while exit_function is False:
                if user_input == "0":
                    exit_function = True

                elif user_input == "1":
                    cls.sub_case1(path_input, language_input, stopwords_input)
                    cls.__print_question_main()
                    user_input = input()

                elif user_input == "2":
                    cls.sub_case2(path_input, language_input, stopwords_input)
                    cls.__print_question_main()
                    user_input = input()

                elif user_input == "3":
                    cls.test_single_description(path_input, language_input, stopwords_input)
                    cls.__print_question_main()
                    user_input = input()

                elif user_input == "4":
                    cls.test_all(path_input, language_input, stopwords_input)
                    cls.__print_question_main()
                    user_input = input()

                else:
                    print("Invalid input! Please enter 0, 1, 2, 3 or 4.")
                    user_input = input()

        except (FileNotFoundError, ValueError) as error:
            sys.exit(str(error))

    @classmethod
    def __print_question_main(cls):
        print("\nPlease choose your next action!")
        print("0: Exit\n"
              "1: Read csv file and start the process \n"
              "2: Test single functions \n"
              "3: Measure possible exaptation for a specific user description and application. \n"
              "4: Measure possible exaptations for a list of applications and applications.")

    @classmethod
    def sub_case1(cls, path_input, language_input, stopwords_input):

        try:
            category_list = CategoryTree.set_up_tree(path_input)
            cls.__print_question_sub_case1()
            user_input = input()

            print("Please name the path of the txt file that contains the user's description")
            user_description = input()

            Validator.check_file_existence(user_description)
            additional_stopwords = NLPHelper.read_additional_stopwords_from_file(stopwords_input)
            exit_function = False

            while exit_function is False:
                if user_input == "0":
                    exit_function = True
                if user_input == "1":
                    cls.sub_case1_1(category_list, language_input, user_description, additional_stopwords)
                    cls.__print_question_sub_case1()
                    user_input = input()
                if user_input == "2":
                    cls.sub_case1_2(user_description, language_input, category_list, additional_stopwords)
                    cls.__print_question_sub_case1()
                    user_input = input()

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def __print_question_sub_case1(cls):
        print("\nPlease choose your next action!")
        print("0: Back\n"
              "1: Use Category CategoryScraper to gather descriptions of all categories (takes more than 1 hour) \n"
              "2: Start from json file that contains keywords for all categories (recommended)")

    @classmethod
    def sub_case1_1(cls, category_list, language_input, user_description, additional_stopwords=None):
        description_dict = CategoryScraper.store_all_descriptions(category_list)
        NLPHelper.initialize_keywords_from_json_all_categories(category_list, "files/dict.json", language_input,
                                                               additional_stopwords)
        keyword_dict_user = NLPHelper.generate_keyword_dict_from_user_description(user_description, language_input,
                                                                                  additional_stopwords)

        print("Please indicate the name of the application you want to measure the distance")
        application_name = input()
        category_comparison = CategoryTree.create_category_profile(application_name, category_list, language_input,
                                                                   additional_stopwords)

        cls.__print_question_sub_case1_1()
        user_input = input()

        exit_function = False

        while exit_function is False:
            if user_input == "0":
                exit_function = True
            if user_input == "1":
                cls.sub_case1_1_1_1(keyword_dict_user)
                cls.__print_question_sub_case1_1()
                user_input = input()
            if user_input == "2":
                cls.sub_case1_1_1_2(category_list, keyword_dict_user)
                cls.__print_question_sub_case1_1()
                user_input = input()
            if user_input == "3":
                cls.sub_case1_1_1_3(category_list, keyword_dict_user)
                cls.__print_question_sub_case1_1()
                user_input = input()
            if user_input == "4":
                cls.sub_case1_1_1_4(category_list, keyword_dict_user, category_comparison)
                cls.__print_question_sub_case1_1()
                user_input = input()

    @classmethod
    def __print_question_sub_case1_1(cls):
        print("\nPlease choose your next action!")
        print("0: Back\n"
              "1: Show keywords for the user's description\n"
              "2: Show best category match for the user's description\n"
              "3: Show Top 10 of the best category matches\n"
              "4: Calculate the distance between the best category match of the user's description and the "
              "initial category of the application\n")

    @classmethod
    def sub_case1_1_1_1(cls, keyword_dict_user):
        print(keyword_dict_user)

    @classmethod
    def sub_case1_1_1_2(cls, category_list, keyword_dict_user):
        best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

        if best_match == -1:
            print("No match found!")
        else:
            print(best_match)

    @classmethod
    def sub_case1_1_1_3(cls, category_list, keyword_dict_user):
        top10 = Calculator.get_top10_best_matches(category_list, keyword_dict_user)
        print(top10)

    @classmethod
    def sub_case1_1_1_4(cls, category_list, keyword_dict_user, category_comparison):
        best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

        if best_match == -1:
            print("Cannot calculate the distance since no matching category was found.")
        else:
            distance = Calculator.calculate_distance(best_match.structure_id, category_comparison.structure_id)
            print(distance)

    @classmethod
    def sub_case1_2(cls, user_description, language_input, category_list, additional_stopwords=None):

        try:
            print('Please name the path of the json file that contains the keywords for all categories.')
            json_file = input()

            Validator.check_file_existence(json_file)

            keyword_dict_user = NLPHelper.generate_keyword_dict_from_user_description(user_description,
                                                                                      language_input,
                                                                                      additional_stopwords)
            NLPHelper.initialize_keywords_from_keywords_dict(category_list, json_file)

            print("Please indicate the name of the application you want to measure the distance")
            application_name = input()
            category_comparison = CategoryTree.create_category_profile(application_name, category_list, language_input,
                                                                       additional_stopwords)

            cls.__print_question_sub_case1_2()
            user_input = input()

            exit_function = False

            while exit_function is False:
                if user_input == "0":
                    exit_function = True
                if user_input == "1":
                    cls.sub_case1_1_2_1(keyword_dict_user)
                    cls.__print_question_sub_case1_2()
                    user_input = input()
                if user_input == "2":
                    cls.sub_case1_1_2_2(category_list, keyword_dict_user)
                    cls.__print_question_sub_case1_2()
                    user_input = input()
                if user_input == "3":
                    cls.sub_case1_1_2_3(category_list, keyword_dict_user)
                    cls.__print_question_sub_case1_2()
                    user_input = input()
                if user_input == "4":
                    cls.sub_case1_1_2_4(category_list, keyword_dict_user, category_comparison, application_name)
                    cls.__print_question_sub_case1_2()
                    user_input = input()

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def __print_question_sub_case1_2(cls):
        print("\nPlease choose your next action!")
        print("0: Back\n"
              "1: Show keywords for the user's description\n"
              "2: Show best category match for the user's description\n"
              "3: Show Top 10 of the best category matches\n"
              "4: Calculate the distance between the best category match of the user's description and the "
              "initial category of the application\n")

    @classmethod
    def sub_case1_1_2_1(cls, keyword_dict_user):
        print(f"The keywords for this description are: {keyword_dict_user}.")

    @classmethod
    def sub_case1_1_2_2(cls, category_list, keyword_dict_user):
        best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

        if best_match == -1:
            print("No match found!")
        else:
            print(f"The best matching category for this description is: {best_match.name}.")

    @classmethod
    def sub_case1_1_2_3(cls, category_list, keyword_dict_user):
        top10 = Calculator.get_top10_best_matches(category_list, keyword_dict_user)
        print(f"The best matching categories for this description are the following: {top10}.")

    @classmethod
    def sub_case1_1_2_4(cls, category_list, keyword_dict_user, category_comparison, application_name):
        best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

        if best_match == -1:
            print("Cannot calculate the distance since no matching category was found.")
        else:
            print(category_comparison)
            category_application_name = ""

            for key in category_comparison:
                category_application_name = key

            category_application = CategoryTree.find_category_by_name(category_list, category_application_name)
            distance = Calculator.calculate_distance(best_match.structure_id, category_application.structure_id)
            print(distance)
            print(f"The distance between the application '{application_name}' ({category_application_name}) "
                  f"and the determined category for the user description is {distance}.")

            if distance >= 4:
                print(f"This specific use of '{application_name}' might be an exaptation.")
            else:
                print(f"This specific use of '{application_name}' is probably not an exaptation.")

    @classmethod
    def sub_case2(cls, path_input, language_input, stopwords):
        category_list = CategoryTree.set_up_tree(path_input)

        cls.__print_question_sub_case2()
        user_input = input()

        exit_function = False

        while exit_function is False:
            if user_input == "0":
                exit_function = True
            if user_input == "1":
                cls.sub_case2_1(language_input, stopwords)
                cls.__print_question_sub_case2()
                user_input = input()
            if user_input == "2":
                cls.sub_case2_2(category_list)
                cls.__print_question_sub_case2()
                user_input = input()
            if user_input == "3":
                cls.sub_case2_3(category_list)
                cls.__print_question_sub_case2()
                user_input = input()
            if user_input == "4":
                cls.sub_case_2_4(language_input, stopwords)
                cls.__print_question_sub_case2()
                user_input = input()

    @classmethod
    def __print_question_sub_case2(cls):
        print("\nPlease choose your next action!")
        print("0: Back\n"
              "1: Use category scraper to gather a description of one category and clean the file\n"
              "2: Show all categories that are stored in the csv file\n"
              "3: Show structure ids of the categories in the csv file\n"
              "4: Extract keywords from file with descriptions for each category.")

    @classmethod
    def sub_case2_1(cls, language_input, additional_stopwords=None):
        print("Please indicate the name of the application you want to scrape the description from "
              "the Play Store. The shown result does not contain any numbers or non ASCII characters (cleaned text).")
        test_category = input()

        success = False
        while success is False:
            try:
                CategoryScraper.get_application_description(test_category)
                success = True
            except:
                pass

        description = NLPHelper.read_description("files/category_description.txt")
        description_cleaned = CategoryScraper.clean_description_file(description)
        print(description_cleaned)
        print("\n")

        cls.__print_question_sub_case2_1()
        user_input = input()

        exit_function = False
        while exit_function is False:
            if user_input == "0":
                exit_function = True
            if user_input == "1":
                cls.sub_case2_1_1(description_cleaned, language_input, additional_stopwords)
                cls.__print_question_sub_case2_1()
                user_input = input()

    @classmethod
    def __print_question_sub_case2_1(cls):
        print("\nDo you want to lemmatize the category description?")
        print("0: No\n"
              "1: Yes")

    @classmethod
    def sub_case2_1_1(cls, description_cleaned, language_input, additional_stopwords=None):
        cls.__print_question_sub_case2_1_1()
        user_input = input()

        exit_function = False
        while exit_function is False:
            if user_input == "0":
                exit_function = True
            if user_input == "1":
                cls.sub_case2_1_1_1(description_cleaned, language_input, additional_stopwords)
                cls.__print_question_sub_case2_1_1()
                user_input = input()
            if user_input == "2":
                cls.sub_case2_1_1_2(description_cleaned, language_input, additional_stopwords)
                cls.__print_question_sub_case2_1_1()
                user_input = input()

    @classmethod
    def __print_question_sub_case2_1_1(cls):
        print("\nPlease choose your next action!")
        print("0: Back\n"
              "1: Show the pos (parts of speech) tags for the category description\n"
              "2: Show Top 15 Tokens that are set as keywords of the category")

    @classmethod
    def sub_case2_1_1_1(cls, description_cleaned, language_input, additional_stopwords=None):
        tokenized_pos_tagged_list = nltk.pos_tag(nltk.word_tokenize(description_cleaned))

        print(f"The following are all non-lemmatized tokens: {tokenized_pos_tagged_list}.")

        list_cleaned = NLPHelper.remove_stopwords_from_pos_tagged_token_list(tokenized_pos_tagged_list,
                                                                             language_input, additional_stopwords)

        print(f"The following are the POS tagged lemmas without stop words: {list_cleaned}.")
        lemmatized_list_relevant = NLPHelper.lemmatize_list(list_cleaned)
        lemmatized_list_relevant = NLPHelper.lemmatize(lemmatized_list_relevant, language_input, additional_stopwords)
        print(f"The following are the lemmas without stop words (only nouns, verbs, adjectives, adverbs): "
              f"{lemmatized_list_relevant}.")

    @classmethod
    def sub_case2_1_1_2(cls, description_cleaned, language_input, additional_stopwords=None):
        tokenized_pos_tagged_list = nltk.pos_tag(nltk.word_tokenize(description_cleaned))

        list_cleaned = NLPHelper.remove_stopwords_from_pos_tagged_token_list(tokenized_pos_tagged_list,
                                                                             language_input, additional_stopwords)
        lemmatized_list_relevant = NLPHelper.lemmatize_list(list_cleaned)
        list_lemmatized_tokens = NLPHelper.lemmatize(lemmatized_list_relevant, language_input, additional_stopwords)
        top15 = NLPHelper.top_tokens(list_lemmatized_tokens, 15)
        top15_normalized = Calculator.calculate_normalized_values_of_keywords(top15)

        print(f"The 15 most common lemmas in the description (absolute number): {top15}.")
        print(f"The 15 most common lemmas in the description (normalized non-rounded values): {top15_normalized}.")

    @classmethod
    def sub_case2_2(cls, category_list):
        CategoryTree.print_categories(category_list)

    @classmethod
    def sub_case2_3(cls, category_list):

        print("All categories with their structure id:")

        for category in category_list:
            print(
                f"'{category.name}' ({category.category_id}) has the structure id: {category.structure_id}.")

        cls.__print_question_sub_case2_3()
        user_input = input()

        exit_function = False
        while exit_function is False:
            if user_input == "0":
                exit_function = True
            if user_input == "1":
                cls.sub_case2_3_1(category_list)
                cls.__print_question_sub_case2_3()
                user_input = input()

    @classmethod
    def __print_question_sub_case2_3(cls):
        print("\nDo you want to calculate the distance between two categories?")
        print("0: No\n"
              "1: Yes")

    @classmethod
    def sub_case2_3_1(cls, category_list):
        print("\nPlease name the categories between which you want to calculate the distance. "
              "The names of the categories must correspond to the names of the categories in the csv file.")
        category_one = input()
        category_two = input()

        try:
            category_1 = CategoryTree.find_category_by_name(category_list, category_one)
            category_2 = CategoryTree.find_category_by_name(category_list, category_two)

            print(f"The distance between '{category_1.name}' and '{category_2.name}' is: "
                  f"{Calculator.calculate_distance(category_1.structure_id, category_2.structure_id)}.")

        except IOError:
            print("One of the categories or both categories do not exist in the csv file. Please check.")

    @classmethod
    def sub_case_2_4(cls, language, stopwords_input):
        try:
            print("\nPlease indicate the name of the json file that contains the descriptions for each category.")
            json_input = input()
            Validator.check_file_existence(json_input)

            additional_stopwords = NLPHelper.read_additional_stopwords_from_file(stopwords_input)

            print('\nThis process may take a little moment (approximately 10 minutes).')

            NLPHelper.generate_keyword_dict(json_input, language, additional_stopwords)

            print("\nKeywords are successfully stored in json file")

        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def test_single_description(cls, csv_input, language_input, stopwords_input):
        try:
            print('Please indicate the path of the json file that contains the keywords for every category.')
            keywords_input = input()
            Validator.check_file_existence(keywords_input)

            print('Please indicate the path of the file where the results should be written to.')
            result_input = input()

            category_list = CategoryTree.set_up_tree(csv_input)
            additional_stopwords = NLPHelper.read_additional_stopwords_from_file(stopwords_input)
            NLPHelper.initialize_keywords_from_keywords_dict(category_list, keywords_input)

            cls.print_start_test()
            user_input = input()
            exit_function = False

            while exit_function is False:
                if user_input == "0":
                    exit_function = True
                if user_input == "1":
                    cls.__request(language_input, additional_stopwords, category_list, result_input)
                    cls.print_start_test()
                    user_input = input()

        except (ValueError, FileNotFoundError) as error:
            sys.exit(str(error))

    @classmethod
    def print_start_test(cls):
        print('Please choose your next action')
        print("0: Back\n"
              "1: Process")

    @classmethod
    def __request(cls, language_input, stopwords_input, category_list, results_path):
        try:
            print('Please indicate the path of the user description')
            user_descriptions_input = input()
            Validator.check_file_existence(user_descriptions_input)

            print('Please indicate the app you want to measure the distance. The name of the app have to match with'
                  'the name of the app in the Play Store!')
            app_input = input()

            keyword_dict_user = NLPHelper.generate_keyword_dict_from_user_description(user_descriptions_input,
                                                                                      language_input, stopwords_input)

            best_matches = CategoryTree.create_category_profile(app_input, category_list, language_input,
                                                                stopwords_input)

            category_name = ""
            for key in best_matches:
                category_name = key

            category_comparison = CategoryTree.find_category_by_name(category_list, category_name)
            best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

            print(f"\nDetermined category for the application '{app_input}': {category_name}")

            if best_match == -1:
                print("No match found!\n")
                line_to_store = user_descriptions_input + ";" + app_input + ";" + category_name + ";No Match" + "\n"

                with open(results_path, 'a') as file:
                    file.write(line_to_store)

            else:
                print(f"Best Match between '{app_input}' and the description: {best_match.name}")

                top10 = Calculator.get_top10_best_matches(category_list, keyword_dict_user)

                print(f"Best Matches between '{app_input}' and the description: {top10}")

                best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)
                distance = Calculator.calculate_distance(best_match.structure_id, category_comparison.structure_id)
                print(f"Distance between the application '{app_input}' and the determined category "
                      f"'{category_comparison.name}': {distance} \n")

                if distance >= 4:
                    print(f"This specific use of '{app_input}' might be an exaptation.\n")
                else:
                    print(f"This specific use of '{app_input}' is probably not an exaptation.\n")

                line_to_store = user_descriptions_input + ";" + app_input + ";" + category_name + ";" + \
                                best_match.name + ";" + str(distance) + ";" + str(top10) + "\n"

                with open(results_path, 'a', encoding='utf-8') as file:
                    file.write(line_to_store)

        except ValueError as error:
            sys.exit(str(error))

    @classmethod
    def test_all(cls, csv_input, language_input, stopwords_input):
        try:
            print('Please indicate the path of the json file that contains the keywords for every category.')
            keywords_input = input()
            Validator.check_file_existence(keywords_input)

            print('Please indicate the path of the file where the results should be written to.')
            result_input = input()

            category_list = CategoryTree.set_up_tree(csv_input)
            additional_stopwords = NLPHelper.read_additional_stopwords_from_file(stopwords_input)
            NLPHelper.initialize_keywords_from_keywords_dict(category_list, keywords_input)

            cls.print_start_test()
            user_input = input()
            exit_function = False

            while exit_function is False:
                if user_input == "0":
                    exit_function = True
                if user_input == "1":
                    cls.__request_test_all(language_input, additional_stopwords, category_list, result_input)
                    cls.print_start_test()
                    user_input = input()
        except ValueError as error:
            sys.exit(str(error))
        except FileNotFoundError as error:
            sys.exit(str(error))

    @classmethod
    def __request_test_all(cls, language_input, stopwords_input, category_list, results_path):
        try:
            with open("files/considered_apps.csv", "r") as read_file:
                lines = csv.reader(read_file, delimiter=";")

                for line in lines:
                    user_descriptions_input = line[0]
                    user_descriptions_input = user_descriptions_input.replace("ï»¿", "")

                    app_input = line[1]

                    keyword_dict_user = NLPHelper.generate_keyword_dict_from_user_description(user_descriptions_input,
                                                                                              language_input,
                                                                                              stopwords_input)
                    best_matches = CategoryTree.create_category_profile(app_input, category_list, language_input,
                                                                        stopwords_input)

                    category_name = ""
                    for key in best_matches:
                        category_name = key

                    category_comparison = CategoryTree.find_category_by_name(category_list, category_name)
                    best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)

                    print(f"\nDetermined category for the application '{app_input}': {category_name}")

                    if best_match == -1:
                        print("No match found!\n")
                        line_to_store = user_descriptions_input + ";" + app_input + ";" + category_name + ";No Match" + "\n"

                        with open(results_path, 'a') as file:
                            file.write(line_to_store)

                    else:
                        print(f"Best Match between '{app_input} and the description': {best_match.name}")

                        top10 = Calculator.get_top10_best_matches(category_list, keyword_dict_user)

                        print(f"Best Matches between '{app_input}' and the description: {top10}")

                        best_match = Calculator.calculate_best_matching_category(category_list, keyword_dict_user)
                        distance = Calculator.calculate_distance(best_match.structure_id,
                                                                 category_comparison.structure_id)
                        print(f"Distance between the application '{app_input}' and the determined category "
                              f"'{category_comparison.name}': {distance} \n")

                        line_to_store = user_descriptions_input + ";" + app_input + ";" + category_name + ";" + \
                                        best_match.name + ";" + str(distance) + ";" + str(top10) + "\n"

                        with open(results_path, 'a', encoding='utf-8') as file:
                            file.write(line_to_store)

        except ValueError as error:
            sys.exit(str(error))
