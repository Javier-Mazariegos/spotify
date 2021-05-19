class Node:
  def __init__(self, data, peso=0):
    self.data = data
    self.peso = peso
    self.next = None

  def __repr__(self):
    return "Peso: " + self.peso


class LinkedList:
  def __init__(self):
    self.head = None

  def __repr__(self):
    node = self.head
    nodes = []
    while node is not None:
        nodes.append(node.data)
        node = node.next
    #nodes.append("None")
    return " --> ".join(nodes)


  def traverse(self):
    node = self.head
    while node is not None:
        print(node.data)
        node = node.next

  def __iter__(self):
    node = self.head
    while node is not None:
        yield node
        node = node.next

  def insert_first(self, node):
    node.next = self.head
    self.head = node

  def remove(self, node_data):
    if self.head is None:
      raise Exception("La lista esta vacia")

    if self.head.data == node_data:
      self.head = self.head.next
      return

    previous_node = self.head

    for node in self:
      if node.data == node_data:
        previous_node.next = node.next
        return

      previous_node = node

    raise Exception("Nodo no existe en la lista")


