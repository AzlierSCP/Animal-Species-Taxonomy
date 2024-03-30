# ----------------------------------------
#  CSC 315 / 615 Spring 2023
#  Project 4 Animal Species Taxonomy
#
#  <<Zihan Gao C23745692>>
# ----------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bisect

# ------------------------------------------
# The TaxonomyNode class
# ------------------------------------------


class TaxonomyNode:
    def __init__(self, name, category):
        self.name = name           # The "name" of the node such as Animalia or Chordata
                                     #   (i.e. the values of the csv table)
        self.category = category   # The "category" such as Kingdom or Phylum
                                     #   (i.e. the column headers of the csv table)
        self.children = []         # The list of children each of type TaxonomyNode

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def addChild(self, name, category):
        # ToDo: function must creat a TaxonomyNode(name,category)
        #       and insert this node into self.children
        #       in sorted order of the name
        new_node = TaxonomyNode(name, category)
        # inserts new_node into self.children in sorted order of the name
        bisect.insort(self.children, new_node)

    def hasChild(self, name, category):
        # ToDo: function returns True if TaxonomyNode(name,category)
        #       is in self.children, and returns False otherwise
        return self.getChild(name, category) is not None

    def getChild(self, name, category):
        # ToDo: add code that returns the child node with a given name,category
        #       it should return None, if no such name,category exists
        index = bisect.bisect_left(self.children, TaxonomyNode(name, category))
        if index != len(self.children) and self.children[index].name == name:
            return self.children[index]
        else:
            return None
# ------------------------------------------
# The TaxonomyTree class
# ------------------------------------------


class TaxonomyTree:
    def __init__(self):
        self.root = TaxonomyNode("", "")

    def addSpecies(self, names, categories):
        # ToDo:  implement code to populate the TaxonomyTree
        #        self.root given the names and categories

        #start at the root node
        current_node = self.root
        for i in range(len(names)):
            #if the current node has a child with the same name and category, move to that child
            if current_node.hasChild(names[i], categories[i]):
                current_node = current_node.getChild(names[i], categories[i])
            #else, add a child with the name and category and move to that child
            else:
                current_node.addChild(names[i], categories[i])
                current_node = current_node.getChild(names[i], categories[i])
    

    @staticmethod
    def print_internal(node, lineno, number_str, name_str):
        # ToDo:  Implement a recursive function to print
        #        the contents of the TaxonomyTree as formatted
        #        to resemble the sample output
        
        if  number_str == "" and name_str == "":
            lineno = 0
        else:
            number_str = number_str + "."
            name_str = name_str + "."
            print(f"{lineno:<10}{number_str:<30}{name_str:}")
        for i ,chlid_node  in enumerate(node.children):
            child_lineno = TaxonomyTree.print_internal(chlid_node, lineno+1, f"{number_str}{i+1}", f"{name_str}{chlid_node.name}")

            lineno = child_lineno
        
        # Return the next lineno for thr parent node
        return lineno
            
        

    def print(self):
        # Do not modify
        TaxonomyTree.print_internal(self.root, 1, "","")

    @staticmethod
    def listScientificNames_internal(node):
        # Extra Credit:  Implement a recursive function to traverse
        #                the TaxonomyTree and return a list of
        #                Scientific Names
        return []

    def printScientificNames(self):
        # Do not modify
        names = TaxonomyTree.listScientificNames_internal(self.root)
        names.sort()
        for name in names:
            print(name)


# ------------------------------------------
# Main code
#   Do not Modify
# ------------------------------------------

# Read the Pandas dataframe
df = pd.read_csv("taxonomy.csv")
rows = df.shape[0]
cols = df.shape[1]
categories = list(df.columns)[1:cols]

# Construct a Taxonomy Tree
tree = TaxonomyTree()

# Insert species into the tree row by row
for r in range(rows):
    names = list(df.iloc[r, 1:cols])
    tree.addSpecies(names, categories)

# Print the contents of the TaxonomyTree
tree.print()

# Extra Credit: print all scientific names in alphabetical order
tree.printScientificNames()
