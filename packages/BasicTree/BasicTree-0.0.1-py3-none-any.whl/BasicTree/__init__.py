"""
Created: July 2018
Updated: December 2018

@author: Andrew Farley
"""
name = "BasicTree"

import random as rand
import math

#This class is for the nodes in the tree, each will have a list of children, a cost, and a data value
class Node:
    def __init__(self):
        self.children = [] #the list of children
        self.cost = rand.randint(0, 9) #the cost to go to this node
        self.data = chr(65+rand.randint(0, 25)) #a random letter assigned as the data value

    #Used to add a child to this node
    #node ----- a node to be pointed to as a child
    def addChild(self, node):
        self.children.append(node)

#This class is the tree itself, you will be able to get the root to perform searches
class Tree:
    def __init__(self, branchingFactor = 2):
        self.root = None
        self.layers = 0
        self.br = branchingFactor
        
    #Returns the root node, useful for performing searches
    def getRoot(self):
        return self.root
    
    #Helper recursive function used by the createTree function
    def createTreeRecursive(self, layers):
        out = Node()
        if (layers > 0):
            for i in range(self.br):
                out.addChild(self.createTreeRecursive(layers-1))
        return out
    
    #Resets a tree and randomizes all data values of nodes 
    #layerNum ----- the number of layers you want the tree to have
    def createTree(self, layerNum):
        self.layers = layerNum-1 #setting the layers variable of the tree
        self.root = self.createTreeRecursive(self.layers) #getting the root node

    #Helper recursive function used by the printTree function
    def printTreeRecursive(self, nodes, layer):
        if (len(nodes) > 0):
            children = []
            adjustVal = int(math.pow(self.br, self.layers-1)/math.pow(self.br, self.layers-layer-1))
            print(' '*(adjustVal+layer), end="")
            for node in nodes:
                print(str(node.data) + ' '*(adjustVal*2), end="")
                children = children + node.children
            print()
            self.printTreeRecursive(children, layer-1)
            return
        else:
            return
            
    #Prints the tree in a hopefully helpful way, used to visualize if searches are performing correctly
    def printTree(self):
        self.printTreeRecursive([self.root], self.layers)
        