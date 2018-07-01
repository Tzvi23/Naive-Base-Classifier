# Author: Tzvi Puchinsky
import csv

class structure_builder:
    """ Builds a Structure Dictionary with attributes and their values """

    def __init__(self):
        self.lines = None
        self.structure = {}
        self.attributes = []
        self.bad_chars = ["{", "}"]  # chars to remove
        self.root_path = ""

    def build_structure(self, root_path):
        """ Gets structure from structure.txt file and loads all the data from train file to lines (list type) """
        self.root_path = str(root_path)
        path = self.root_path + "/Structure.txt"
        fh = open(path, "r")
        data = fh.readlines()

        for line in data:
            words = line.split()
            self.attributes.append(words[1])
            if words[2] == "NUMERIC":
                self.structure[words[1]] = "NUMERIC"
            else:
                self.structure[words[1]] = str(filter(lambda x: x not in self.bad_chars, words[2])).split(",")
        print self.structure
        print self.attributes
        fh.close()

        train_path = self.root_path + "/train.csv"
        read = csv.reader(open(train_path))
        self.lines = list(read)

    def get_structure(self):
        """ Returns structure """
        return self.structure

    def get_attributes(self):
        """ Returns attributes """
        return self.attributes

    def get_lines(self):
        """ Returns lines """
        return self.lines