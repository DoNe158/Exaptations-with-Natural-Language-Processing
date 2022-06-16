import re
import sys
import json
import nltk

from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from application.Validator import Validator


def read_description_string(description):
    """
    Reads a description (string) and converts the text in ASCII. All non-ASCII characters are removed.
    Moreover, all characters are set to lower case characters.

    :param description: description for a specific category.
    :return: ASCII formatted string in lower case.
    """

    try:
        Validator.check_empty_string(description)
        file_only_ascii = description.encode("ascii", "ignore")
        text = file_only_ascii
        text = text.lower()
        text = text.decode('utf-8')
        new_string = " ".join(text.splitlines())
        return new_string

    except ValueError as error:
        sys.exit(str(error))


def read_description(file_description) -> str:
    """
    Reads the description of the given file and converts the text in ASCII. All non-ASCII characters are removed.
    Moreover, all characters are set to lower case characters.

    :param file_description: file with the description for a specific category.
    :return: ASCII formatted string in lower case.
    """

    try:
        with open(file_description, "r", encoding="mbcs") as text_file:
            file = text_file.read()
            file_only_ascii = str(file)
            file_only_ascii = file_only_ascii.encode("ascii", "ignore")
            text = file_only_ascii
            text = text.lower()
            text = text.decode('utf-8')
            new_string = " ".join(text.splitlines())
            return new_string

    except OSError as error:
        sys.exit(str(error))


def clean_file(text_for_cleaning) -> str:
    """
    Removes all links to websites (http, https, www), email addresses as well as special characters in ASCII.

    :param text_for_cleaning: string where websites, email addresses, and special characters are removed.
    :return: string without any links to websites, email addresses, and special characters.
    """

    try:
        Validator.check_empty_string(text_for_cleaning)

        text_cleaned = re.sub(r"http\S+", "", text_for_cleaning)
        text_cleaned = re.sub(r"www\S+", "", text_cleaned)
        text_cleaned = re.sub(r"\S*@\S*\s?", "", text_cleaned)
        text_cleaned = re.sub(r'[-.?!,:;()|0-9+&"/%$*=]', '', text_cleaned)
        return text_cleaned

    except ValueError as error:
        sys.exit(str(error))


def top_tokens(token_list, number_of_tokens) -> dict:
    """
    Calculates the most common tokens in the given list containing tokenized words. The number of tokens to be
    displayed must be given as the second parameter.

    :param token_list: list containing tokenized words.
    :param number_of_tokens: number of the most common tokens that is needed.
    :return: dictionary containing the most common tokens including the frequency of their occurrences.
    """

    freq_dist = FreqDist()
    token_dict = dict()

    for token in token_list:
        freq_dist[token.lower()] += 1

    most_common = freq_dist.most_common(number_of_tokens)
    for element in most_common:
        token_dict[element[0]] = element[1]

    return token_dict


def remove_stopwords_from_pos_tagged_token_list(pos_tagged_token_list, language, additional_stopwords=None) -> list:
    """
    Removes punctuation, numbers, and stopwords from a given list of tuples containing a token (at index 0)
    and its part of speech tag (at index 1).

    :param pos_tagged_token_list: list with tuples containing tokens with their pos tags.
    :param language: language of the text to be analyzed.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the already
    defined stopwords by the nltk package.
    :return: list of tuples containing only the tokens that are not numbers or stopwords.
    """

    try:
        Validator.check_empty_list(pos_tagged_token_list)
        Validator.check_language(language)

        stop_words = set(stopwords.words(language))

        if additional_stopwords is not None:
            additional_stopwords = additional_stopwords.lower().replace(" ", "")
            additional_stopwords = additional_stopwords.split(',')
            stop_words.update(additional_stopwords)

        punctuation = re.compile(r'[-.?!,:;()|0-9]')
        token_list_post_punctuation = []
        pos_tagged_token_list_cleaned = []

        for word in pos_tagged_token_list:
            tmp = punctuation.sub("", word[0])
            if len(tmp) > 0:
                token_list_post_punctuation.append(word)

        for word in token_list_post_punctuation:
            if word[0] not in stop_words:
                pos_tagged_token_list_cleaned.append(word)

        return pos_tagged_token_list_cleaned

    except ValueError as error:
        sys.exit(str(error))


def define_pos_tag(tag):
    """
    Checks the part of speech and converts the different forms of nouns, verb, adjectives and adverbs to a simpler
    form. Tokens of the other parts of speech do not carry enough meaning. Therefore, they are not considered.

    :param tag: part of speech tag that are used within the lemmatizer of NLTK.
    :return: part of speech tag in a simpler notation.
    """
    if tag in ['NN', 'NNP', 'NNPS', 'NNS']:
        return 'n'
    elif tag in ['VB', 'VBD', 'VBN', 'VBP', 'VBZ', 'VBG']:
        return 'v'
    elif tag in ['JJ', 'JJR', 'JJS']:
        return 'a'
    elif tag in ['RB', 'RBR', 'RBS']:
        return 'r'
    else:
        return None


def lemmatize_list(list_with_lemmatized_tokens) -> list:
    """
    Lists only the tokens with the part of speech 'noun', 'verb', 'adjective', and 'adverb'. Tokens with parts of
    speech different that the mentioned ones are not considered.

    :param list_with_lemmatized_tokens: list of tokens that are tagged with their parts of speech.
    :return: list of tokens that are nouns, verbs, adjectives, and adverbs only.
    """

    try:
        Validator.check_empty_list(list_with_lemmatized_tokens)

        list_specific_tokens = []

        for token, tag in list_with_lemmatized_tokens:
            result = define_pos_tag(tag)
            if result is not None:
                list_specific_tokens.append((token, result))

        return list_specific_tokens

    except ValueError as error:
        sys.exit(str(error))


def lemmatize(list_with_pos_tagged_tokens, language, additional_stopwords=None) -> list:
    """
    Lemmatizes a given list containing tokens with their part of speech tags which do have to correspond
    to the pos tags of the nltk framework ('n' for noun, 'v' for verb, 'a' for adjective, 'r' for adverb).

    :param list_with_pos_tagged_tokens: list of tokens with their part of speech tags.
    :param language: language of the description.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    :return: list of tokens in their lemmatized form.
    """

    try:
        Validator.check_empty_list(list_with_pos_tagged_tokens)
        Validator.check_language(language)

        lemmatizer = WordNetLemmatizer()
        lemmatized_content = []
        list_lemma = []

        for token, tag in list_with_pos_tagged_tokens:
            lemmatized_content.append(lemmatizer.lemmatize(token, tag))

        stop_words = set(stopwords.words(language))

        if additional_stopwords is not None:
            additional_stopwords = additional_stopwords.lower().replace(" ", "")
            additional_stopwords = additional_stopwords.split(',')
            stop_words.update(additional_stopwords)

        for word in lemmatized_content:
            if word not in stop_words:
                list_lemma.append(word)

        return list_lemma

    except ValueError as error:
        sys.exit(str(error))


def generate_keyword_list_from_string(description, language, additional_stopwords=None) -> list:
    """
    Reads a file with a description, cleans the description and converts it into a lemmatized list containing tokens
    that are nouns, verbs, adjectives and adverbs.
    The parts of speech tagging corresponds to the NLTK parts of speech tagging.

    :param description: description to be read.
    :param language: language of the description.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    :return: list of lemmatized tokens.
    """

    try:
        Validator.check_language(language)

        text = read_description_string(description)
        text = clean_file(text)
        tokenized_pos_tagged_list = nltk.pos_tag(nltk.word_tokenize(text))

        list_cleaned = remove_stopwords_from_pos_tagged_token_list(tokenized_pos_tagged_list, language)
        lemmatized_list_relevant = lemmatize_list(list_cleaned)
        list_lemmatized_tokens = lemmatize(lemmatized_list_relevant, language, additional_stopwords)

        return list_lemmatized_tokens

    except ValueError as error:
        sys.exit(str(error))


def generate_keyword_list(description, language, additional_stopwords=None) -> list:
    """
    Reads a file with a description, cleans the description and converts it into a lemmatized list containing tokens
    that are nouns, verbs, adjectives and adverbs.
    The parts of speech tagging corresponds to the NLTK parts of speech tagging.

    :param description: description to be read.
    :param language: language of the description.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    :return: list of lemmatized tokens.
    """

    try:
        Validator.check_file_existence(description)
        Validator.check_language(language)

        text = read_description(description)
        text = clean_file(text)
        tokenized_pos_tagged_list = nltk.pos_tag(nltk.word_tokenize(text))

        list_cleaned = remove_stopwords_from_pos_tagged_token_list(tokenized_pos_tagged_list, language)
        lemmatized_list_relevant = lemmatize_list(list_cleaned)
        list_lemmatized_tokens = lemmatize(lemmatized_list_relevant, language, additional_stopwords)
        return list_lemmatized_tokens

    except (FileNotFoundError, ValueError) as error:
        sys.exit(str(error))


def initialize_keywords(category, description, language, additional_stopwords=None):
    """
    Generates a keywords list based on the several methods using a file with descriptions and the language setting for
    those descriptions and sets the 15 most frequent keywords of this list as the keywords of the given category.

    :param category: Category for which the keywords should be set.
    :param description: file that contains descriptions of the category.
    :param language: language of the description in the file.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    """

    try:
        Validator.check_existence_category(category)
        Validator.check_file_existence(description)
        Validator.check_language(language)

        keywords_list = generate_keyword_list(description, language, additional_stopwords)
        keywords_dict = top_tokens(keywords_list, 15)
        category.set_keywords(keywords_dict)

    except (FileNotFoundError, ValueError) as error:
        sys.exit(str(error))


def initialize_keywords_from_json(category, json_file, language, additional_stopwords=None):
    """
    Generates a keywords list based on the several methods using a file with descriptions and the language setting for
    those descriptions and sets the 15 most frequent keywords of this list as the keywords of the given category. The
    descriptions are stored in a json file that is read at the beginning.

    :param category: Category for which the keywords should be set.
    :param json_file: file that contains descriptions of the category.
    :param language: language of the description in the file.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    """

    try:
        Validator.check_existence_category(category)
        Validator.check_file_existence(json_file)
        Validator.check_language(language)

        with open(json_file) as f:
            try:
                data = json.load(f)
            except:
                raise ValueError('No valid json format.')

            data = data[category.name]
            tokenized_pos_tagged_list = nltk.pos_tag(nltk.word_tokenize(data))

            list_cleaned = remove_stopwords_from_pos_tagged_token_list(tokenized_pos_tagged_list, language)
            lemmatized_list_relevant = lemmatize_list(list_cleaned)
            list_lemmatized_tokens = lemmatize(lemmatized_list_relevant, language, additional_stopwords)
            keywords_list = top_tokens(list_lemmatized_tokens, 15)
            category.set_keywords(keywords_list)

    except (FileNotFoundError, ValueError) as error:
        sys.exit(str(error))


def generate_keyword_dict(json_file, language, additional_stopwords=None):
    """
    Reads a json file that contains all names of the categories and their descriptions. After that, for every category
    the 15 most common keywords are calculated based on the description and stored in a dictionary that is saved as
    a json file that can be used for setting the keywords of each category.

    :param json_file: json file that contains all category names and their descriptions.
    :param language: language of the descriptions.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    """

    try:
        Validator.check_file_existence(json_file)
        Validator.check_language(language)

        with open(json_file) as f:
            try:
                description_dict = json.load(f)
            except:
                raise ValueError('No valid json format.')

            keyword_dict = dict()

            data_dict = description_dict.items()
            for key, value in data_dict:
                if key != 'Category':
                    key_new = key
                    if additional_stopwords == "":
                        keywords_list = generate_keyword_list_from_string(value, language)
                    else:
                        keywords_list = generate_keyword_list_from_string(value, language, additional_stopwords)
                    keywords_dict = top_tokens(keywords_list, 15)
                    value_new = keywords_dict
                    keyword_dict.__setitem__(key_new, value_new)

            with open('files/keywords_dictionaries.json', 'w') as path:
                json.dump(keyword_dict, path)

    except (FileNotFoundError, ValueError) as error:
        sys.exit(str(error))


def initialize_keywords_from_keywords_dict(category_list, json_file):
    """
    Reads a json file containing all keywords with their occurrences for each category and sets those keywords to
    their respective category.

    :param category_list: list of type Category that contains all categories.
    :param json_file: json file containing the keywords for each category.
    """

    try:
        Validator.check_empty_list(category_list)
        Validator.check_file_existence(json_file)

        with open(json_file) as f:
            try:
                keywords_dict = json.load(f)
            except:
                raise ValueError('No valid json format.')

        for category in category_list:
            if category.name != 'Category':
                keywords = keywords_dict[category.name]
                category.set_keywords(keywords)

    except (ValueError, FileNotFoundError) as error:
        sys.exit(str(error))


def generate_keyword_dict_from_user_description(description_file, language, additional_stopwords=None):
    """
    Generates a keyword dictionary from the description in the given file consisting of the token and the frequency.

    :param description_file: text file containing the description of the user.
    :param language: language of the description.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    :return: dictionary of tokenized and lemmatized keywords of the user's description.
    """

    try:
        Validator.check_file_existence(description_file)
        Validator.check_language(language)

        keyword_list = generate_keyword_list(description_file, language, additional_stopwords)
        keyword_dict = top_tokens(keyword_list, len(keyword_list))
        return keyword_dict

    except (FileNotFoundError, ValueError) as error:
        sys.exit(str(error))


def initialize_keywords_from_json_all_categories(category_list, json_file, language, additional_stopwords=None):
    """
    Initializes the keywords for all categories in the category tree.

    :param category_list: list of type Category that contains all categories.
    :param json_file: file that contains all descriptions of the category.
    :param language: language of the description.
    :param additional_stopwords: string containing additional stopwords that can be set in addition to the stopwords
    defined in the nltk package.
    """

    try:
        Validator.check_empty_list(category_list)
        Validator.check_file_existence(json_file)
        Validator.check_language(language)

        for category in category_list:
            if category.name != 'Category':
                initialize_keywords_from_json(category, json_file, language, additional_stopwords)

    except (ValueError, FileNotFoundError) as error:
        sys.exit(str(error))


def read_additional_stopwords_from_file(path):
    """
    Reads additional stop words from a txt file. Every stop word has to be separated by a line break at the end. Only
    one stop word per line.

    :param path: path of the file that contains the additional stop words.
    :return: string containing additional stop words.
    """

    with open(path, "r", encoding="mbcs") as stopwords_file:
        try:
            additional_stopwords = stopwords_file.read().replace("\n", ",")
            return additional_stopwords

        except FileNotFoundError:
            return "The file was not found."
