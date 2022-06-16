class Category:

    def __init__(self, category_id, name):
        """
        Initially, only the category id and the name is set. Furthermore, an empty list is initialized for
        the children. The other attributes are of type 'None' and will be filled within other functions.

        :param category_id: id of the category as it is defined in the csv file.
        :param name: name of the category as it is defined in the csv file.
        """

        self.category_id = category_id
        self.name = name
        self.parent = None
        self.children = []
        self.parent_id = None
        self.keywords = dict()
        self.tier = ""
        self.structure_id = 0

    def get_tier(self):
        """
        Gets the tier of a category.
        :return: tier
        """

        return self.tier

    def get_parent(self):
        """
        Gets the parent of a category.
        :return: parent
        """

        return self.parent

    def set_tier(self, tier):
        """
        Sets the tier of the category depending on the Category Tree in which the category is stored.

        :param tier: level of depth in the Category Tree.
        """
        self.tier = tier

    def set_structure_id(self, structure_id):
        """
        Sets the structure id of the category that represents the position within in the category tree.

        :param structure_id: specific id that depends on the depth and the amount of categories that are children of
        a specific category.
        """

        self.structure_id = structure_id

    def set_parent_id(self, parent_id):
        """
        Sets the parent id of the category.

        :param parent_id: id of the parent.
        """

        self.parent_id = parent_id

    def set_keywords(self, keywords_dict):
        """
        Sets a given list with keywords as the default keywords for this category.

        :param keywords_dict: list containing keywords of this category.
        """
        self.keywords = keywords_dict
