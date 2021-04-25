from flask.helpers import url_for
from memory_profiler import profile
from flask import Flask, request
from jinja2 import Template, Environment, FileSystemLoader
import csv
import cProfile
from linkedlist import Cancion, LinkedList
from queue import Queue

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)

listadoCanciones = LinkedList()
colaCanciones = Queue()
listaCanciones = []
colaLista = []
cancionActual = " "
ultimaCancion = None



def añadirCancion(nombre,artista,album)-> None:
    datos = ["","",""]
    datos[0] = nombre
    datos[1] = artista
    datos[2] = album
    with open('listado.csv','a',newline='') as writeFile:
        writer = csv.writer(writeFile,delimiter=",",quotechar=',',quoting=csv.QUOTE_MINIMAL,lineterminator='')
        writer.writerow('\n')
        writer.writerow(datos)
    listaCanciones.append(Cancion(datos[0],datos[1],datos[2]))
    listadoCanciones.insertar(datos[0],datos[1],datos[2])

def eliminarCancion():
    cont = -1
    i = 0
    lista = ["","",""]
    cancion = listadoCanciones.head
    with open('listado.csv') as File:
        reader = csv.reader(File,delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            cont = cont+1
    with open('listado.csv','w',newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", quotechar=',',quoting=csv.QUOTE_MINIMAL,lineterminator='')
        while (i != cont):
            lista[0] = cancion.nombre
            lista[1] = cancion.artista
            lista[2] = cancion.album
            if (i != 0):
                writer.writerow('\n')
            writer.writerow(lista)
            cancion = cancion.next
            i+=1


def cargarCanciones():
    global listadoCanciones, listaCanciones
    with open('listado.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            datos = row
            #if contador == 0:
            #    listadoCanciones.push(datos[0],datos[1],datos[2])
            #else:
            listaCanciones.append(Cancion(datos[0],datos[1],datos[2]))
            listadoCanciones.insertar(Cancion(datos[0],datos[1],datos[2]))

def cola_a_Lista():
    global colaLista, colaCanciones
    colaLista = []
    if colaCanciones.is_empty1() == False:
        currentNode = colaCanciones.head
        while (True):
            if currentNode.next is not None or colaCanciones.is_empty1() == False:
                colaLista.append(currentNode)
                if currentNode.next is not None:
                    currentNode = currentNode.next
                else:
                    break
            else:
                break
def actulizarListaCanciones():
    global listadoCanciones, listaCanciones
    listaCanciones = []
    if listadoCanciones.head is not None:
        currentNode = listadoCanciones.head
        while(True):
            if currentNode.next != listadoCanciones.head or currentNode.next is not None or currentNode == listadoCanciones.head:
                listaCanciones.append(currentNode)
                if currentNode.next is not None:
                    currentNode = currentNode.next
                else:
                    break
            else:
                break
        


def deletequeue(cancion_eliminar, cancion):
    global colaCanciones
    contador = 0
    while (True):
        if cancion is not None:
            if cancion_eliminar == colaCanciones.head.nombre:
                colaCanciones.dequeue()
                break
            if contador == 1:
                cancion_comprobacion = colaCanciones.head
            if cancion_eliminar == cancion.nombre:
                cancion_comprobacion.next = cancion.next
                break
            else:
                cancion = cancion.next
                if contador >=1:
                    cancion_comprobacion = cancion_comprobacion.next
                contador = contador + 1
        else:
            break
    cola_a_Lista()

def deletelist(cancion_eliminar, cancion):
    while (True):
        if cancion.next is not None:
            if cancion_eliminar == listadoCanciones.head.nombre:
                listadoCanciones.head = listadoCanciones.head.next
                break
            if cancion_eliminar == cancion.nombre:
                cancion.next.previous = cancion.previous
                cancion.previous.next = cancion.next
                break
            else:
                cancion = cancion.next
        else:
            break
    eliminarCancion()

cargarCanciones()
#principal
@app.route('/', methods=["GET","POST"], endpoint='index')
def index():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    contador = 0 
    css = url_for('static', filename='micss.css')
    #cambiar cancion
    if(request.method == "POST"):
        if request.form.get('Play Previous') == 'Play Previous':
            if(cancionActual.nombre != ultimaCancion.nombre):
                cancionActual = ultimaCancion
            else:
                if(cancionActual.previous is None):
                    pass
                else:
                    cancionActual = cancionActual.previous
                    ultimaCancion = cancionActual

        elif request.form.get('Play Next') == 'Play Next':
            if colaCanciones.is_empty1() == True:
                if(ultimaCancion.next == listadoCanciones.head or ultimaCancion.next is None):
                    cancionActual = listadoCanciones.head
                    ultimaCancion = cancionActual
                else:
                    cancionActual = ultimaCancion.next
                    ultimaCancion = cancionActual
            else:
                cancionActual = colaCanciones.dequeue()
        elif request.form.get('play nueva') == 'play nueva':
            cancion_nueva = request.form.get('nombre cancion')
            if cancionActual != cancion_nueva:    
                cancion = listadoCanciones.head
                while (True):
                    if cancion.next is not None:
                        if cancion_nueva == cancion.nombre:
                            cancionActual = cancion
                            ultimaCancion = cancionActual
                            break
                        else:
                            cancion = cancion.next
                    else:
                        break
            else:
                pass

        #Agregar a la cola
        elif request.form.get('agregar') == 'agregar':
            cancion_nueva = request.form.get('nombre cancion')
            cancion = listadoCanciones.head
            while (True):
                if cancion.next is not None:
                    if cancion_nueva == cancion.nombre:
                        colaCanciones.enqueue(cancion)
                        break
                    else:
                        cancion = cancion.next
            cola_a_Lista()
        #se reproduce la primera cancion
        elif request.form.get('play') == 'play':
            if cancionActual == " ":
                cancionActual = listadoCanciones.head
                ultimaCancion = cancionActual
            #xCancion = Cancion("Levitating", "Dua Lipa", "Future Nostalgia")
            #colaCanciones.enqueue(xCancion)
            #deletequeue(xCancion.nombre, colaCanciones.head)
        elif request.form.get('delete_queue') == 'delete_queue':
            cancion_eliminar = request.form.get('nombre cancion')
            cancion = colaCanciones.head
            deletequeue(cancion_eliminar, cancion)
            cola_a_Lista()
        elif request.form.get('delete_list') == 'delete_list':
            cancion_eliminar = request.form.get('nombre cancion')
            cancion = listadoCanciones.head
            deletequeue(cancion_eliminar, colaCanciones.head)
            deletelist(cancion_eliminar, cancion)
            actulizarListaCanciones()
        elif request.form.get('añadir_cancion') == 'añadir_cancion':
            nombre_cancion = request.form.get('nombre cancion')
            artista = request.form.get('artista')
            album = request.form.get('album')
            añadirCancion(nombre_cancion,artista,album)
        else:
            pass

        template = env.get_template('spoti.html')
        return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion=cancionActual.nombre,nombreArtista=cancionActual.artista,nombreAlbum=cancionActual.album,style_sheet=css )
    template = env.get_template('spoti.html')
    return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion="---",nombreArtista="---",nombreAlbum="---", style_sheet=css)

if __name__ == '__main__':
    app.run(debug=True)

#cProfile.run("listadoCanciones.insertar('The Show Must Go On','Queen','Innuendo')")
#cProfile.run("añadirCancion('The Show Must Go On','Queen','Innuendo')")
#cProfile.run("cargarCanciones()")