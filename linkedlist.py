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

    def insertar(self,nombre,artista,album):
        nuevaCancion = Cancion(nombre,artista,album)
        nuevaCancion.next = None
        if self.head is None:
            self.head = nuevaCancion
            return
        last = self.head
        while (last.next is not None):
            last = last.next
        last.next = nuevaCancion
        nuevaCancion.previous = last
        nuevaCancion.next = self.head
        return
