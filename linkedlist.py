class Cancion:
    def __init__(self, nombre, artista, album):
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.previous = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def insertar(self, cancion):
        if self.head is None:
            self.head = cancion
        else:
            for current_node in self:
                pass
            current_node.next = cancion
            cancion.previous = current_node