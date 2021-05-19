from linked_list import LinkedList, Node
from random import randint

class Graph:
  def __init__(self):
    self.adjacency_lists = {}

  def __repr__(self):
    g = ""
    for element in self.adjacency_lists:
      for x in self.adjacency_lists[element]:
        g += element + " = {} => ".format(x.peso) + x.data + ";  "
      g += "\n"


    return g

  def add_node(self, node_label):
    self.adjacency_lists[node_label] = LinkedList()

  def add_edge(self, start_node, end_node, weight):
    n = Node(end_node, weight)
    self.adjacency_lists[start_node].insert_first(n)
  def updatepeso(self):
    for element in self.adjacency_lists:
      for x in self.adjacency_lists[element]:
        x.peso = randint(1,9)
  def path_exists(self, start, end):
    return True

  def path_under_2_moves(self, start, end):
    return False


