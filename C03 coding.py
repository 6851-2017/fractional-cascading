# jamb
# C02 CODING: Orthogonal Range Searching

import random


class Node:
    def __init__(self, value):
        self.value = value
        self.out_edges = []
        self.in_edges = []

    def add_edge(self, n2):
        self.out_edges.append(n2)
        n2.in_edges.append(self)

    def __str__(self):
        return str(self.value)


class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes

    def add_node(self, n):
        self.nodes.append(n)

    # directed edge from n1 to n2
    def add_edge(self, n1, n2):
        if n1 not in self.nodes:
            self.nodes.append(n1)
        if n2 not in self.nodes:
            self.nodes.append(n2)
        n1.add_edge(n2)

    def __str__(self):
        out = ""
        for node in self.nodes:
            out += str(node) + "->{" + ",".join([str(x) for x in node.out_edges]) + "}\n"
        return out
        

# test Graphs
n1 = Node("x")
n2 = Node("b")
g1 = Graph([n1, n2])
g1.add_node(Node("c"))
g1.add_edge(n1, n2)
print(g1)

# starting with the example problem of k lists to search in (linear graph)
# TODO will expand from there

class CascadeNode:
    def __init__(self, value):
        self.value = value
        self.successor = None
        self.predecessor = None
        self.parent = None  # the one in a different linked list that's the same
        # TODO actually maintain the next two
        self.next_real_item = None  # if it was in the original list, itself; if not, the next one that was
        self.prev_real_item = None  # if it was in the original list, itself; if not, the previous one that was

    def link(self, n2):
        self.successor = n2
        n2.predecessor = self

    def __str__(self):
        if not self.successor:
            return str(self.value)
        return str(self.value) + " -> " + str(self.successor)
            

class Cascader:
    def __init__(self, list_of_lists, alpha=2):
        self.lists = list_of_lists
        self.n = max([len(l) for l in self.lists])
        self.k = len(self.lists) # goal is O(k + log n) search
        self.alpha = alpha  # 1/alpha = fraction of elts to cascade
        self.extended_lists = [] # linked lists of Nodes
        self.extend_lists()

    # for each list, put some fraction 1/alpha of its elements into the next list
    # and connect pointers from it back to the originals
    def extend_lists(self):
        nl = []  # nodes from the previous extended linked list that are getting cascaded up
        for l in self.lists:
            recent_node = None
            l_index = 0
            nl_index = 0
            
            if not nl or l[0] < nl[0].value:
                l_val = l[l_index]
                recent_node = CascadeNode(l_val)
                l_index += 1
            else:
                nl_val = nl[nl_index].value
                recent_node = CascadeNode(nl_val)
                recent_node.parent = nl[nl_index]
                nl_index += 1
            new_extended_list = recent_node  # the next extended linked list points to the first node in itself
            # merge stuff together and construct nodes
            while (l_index < len(l) and nl_index < len(nl)): # merge stuff
                if l[l_index] < nl[nl_index].value:
                    l_val = l[l_index]
                    next_node = CascadeNode(l_val)
                    recent_node.link(next_node)
                    recent_node = next_node
                    l_index += 1
                else:
                    nl_val = nl[nl_index].value
                    next_node = CascadeNode(nl_val)
                    next_node.parent = nl[nl_index]
                    recent_node.link(next_node)
                    recent_node = next_node
                    nl_index += 1
                
            # add in the stuff that didn't get merged
            if l_index < len(l):
                for elem in l[l_index:]:
                    next_node = CascadeNode(elem)
                    recent_node.link(next_node)
                    recent_node = next_node
            else:
                for elem in nl[nl_index:]:
                    next_node = CascadeNode(elem.value)
                    recent_node.link(next_node)
                    next_node.parent = elem
                    recent_node = next_node
            
            self.extended_lists.append(new_extended_list)  # we finished determining this level
            nl = []  # find things we'll cascade to the next level
            count = 0
            x = new_extended_list
            while x is not None:
                if count % self.alpha == 0:
                    nl.append(x)
                count += 1
                x = x.successor

    def find(self, x):
        # get x's predecessor/successor in every list, and return a list of those pairs
        extended_pred_succ = self.find_in_extended_lists(x)
        return [(x.prev_real_item, y.next_real_item) for (x,y) in extended_pred_succ]        

    def find_in_extended_lists(self, x):
        # get x's predecessor/successor in every extended list, and return a list of those pairs
        (pred, succ) = self.find_in_last_list(x)
        # TODO

    def find_in_last_list(self, x):
        # find x in the last list (the longest one), extended_lists[-1]; return (pred, succ)
        l = self.extended_lists[-1]
        # TODO do something better than a linked list so this is O(logn) not O(n)...
        pred = l
        while (pred.successor.value < x):
            pred = pred.successor
        succ = pred.successor
        if succ.value == x:
            pred = succ
        return (pred, succ)


# TEST CASE
n = 10
k = 4
lists = [sorted([random.randint(0,100) for x in range(n)]) for x in range(k)]
print("\n".join([str(x) for x in lists]))
print()

casc = Cascader(lists)
print("\n".join([str(x) for x in casc.extended_lists]))
        
    
