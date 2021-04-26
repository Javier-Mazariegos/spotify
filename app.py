from flask.helpers import url_for
from memory_profiler import profile
from flask import Flask, request
from jinja2 import Template, Environment, FileSystemLoader
import csv
import unittest
import time 
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


@profile
def añadirCancion(nombre,artista,album)-> None:
    global listadoCanciones
    datos = ["","",""]
    datos[0] = nombre
    datos[1] = artista
    datos[2] = album
    with open('listado.csv','a',newline='') as writeFile:
        writer = csv.writer(writeFile,delimiter=",",quotechar=',',quoting=csv.QUOTE_MINIMAL,lineterminator='')
        writer.writerow('\n')
        writer.writerow(datos)
    #listaCanciones.append(Cancion(datos[0],datos[1],datos[2]))
    listadoCanciones.insertar(Cancion(datos[0],datos[1],datos[2]))
    comprobadorListadoTrue(datos[0])

def contadorListado(nombreCancion):
    global listadoCanciones
    comprobacion = False
    for c in listadoCanciones:
        if nombreCancion == c.nombre:
            comprobacion = True
    return comprobacion

def contadorQueue(nombreCancion):
    comprobacion = False
    if colaCanciones.is_empty1() == False:
        currentNode = colaCanciones.head
        while (True):
            if currentNode.next is not None or colaCanciones.is_empty1() == False:
                if currentNode.next is not None:
                    if nombreCancion == currentNode.nombre:
                        comprobacion = True
                        break
                    currentNode = currentNode.next
                else:
                    break
            else:
                return comprobacion
                break
    return comprobacion

def comprobadorListadoTrue(nombreCancion):
    resultado = contadorListado(nombreCancion)
    assert resultado == True, "Debe ser 'True'"

def comprobadorListadoFalse(nombreCancion):
    resultado = contadorListado(nombreCancion)
    assert resultado == False, "Debe ser 'False'"
    
def comprobadorQueueTrue(nombreCancion):
    resultado = contadorQueue(nombreCancion)
    assert resultado == True, "Debe ser 'True'"

def comprobadorQueueFalse(nombreCancion):
    resultado = contadorQueue(nombreCancion)
    assert resultado == False, "Debe ser 'False'"


@profile
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

@profile
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
            comprobadorListadoTrue(datos[0])

@profile
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

@profile
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
        
@profile
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
    start_time = time.time()
    cola_a_Lista()
    print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    comprobadorQueueFalse(cancion_eliminar)


@profile
def deletelist(cancion_eliminar, cancion):
    global listadoCanciones
    for nodo in listadoCanciones:
        if (cancion_eliminar == cancion.nombre):
            listadoCanciones.head = cancion.next
            break
        elif (nodo.nombre == cancion_eliminar):
            nodo.previous.next = nodo.next
            if nodo.next is not None:
                nodo.next.previous = nodo.previous
            break
        else:
            nodo = nodo.next
    start_time = time.timme()
    eliminarCancion()
    print("Time en 'eliminarCancion': %s  seconds " %(time.time() - start_time))
    comprobadorListadoFalse(cancion_eliminar)
    comprobadorQueueFalse(cancion_eliminar)

start_time = time.time()
cargarCanciones()
print("Time en 'cargarCanciones': %s  seconds " %(time.time() - start_time))
#principal
@app.route('/', methods=["GET","POST"], endpoint='index')
@profile
def index():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    contador = 0 
    css = url_for('static', filename='micss.css')
    #cambiar cancion
    if(request.method == "POST"):
        if 'Play Previous' in request.form:
            if(cancionActual.nombre != ultimaCancion.nombre):
                cancionActual = ultimaCancion
            else:
                if(cancionActual.previous is None):
                    pass
                else:
                    cancionActual = cancionActual.previous
                    ultimaCancion = cancionActual
            start_time = time.time()
            cola_a_Lista()
            print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
        elif 'Play Next' in request.form:
            if colaCanciones.is_empty1() == True:
                if(ultimaCancion.next == listadoCanciones.head or ultimaCancion.next is None):
                    cancionActual = listadoCanciones.head
                    ultimaCancion = cancionActual
                else:
                    cancionActual = ultimaCancion.next
                    ultimaCancion = cancionActual
            else:
                cancionActual = colaCanciones.dequeue()
            start_time = time.time()
            cola_a_Lista()
            print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
        elif 'play nueva' in request.form:
            cancion_nueva = request.form['play nueva']
            if cancionActual != cancion_nueva:    
                cancion = listadoCanciones.head
                while (True):
                    if cancion.next is not None or cancion.next != listadoCanciones.head:
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
        elif 'agregar' in request.form:
            cancion_nueva = request.form['agregar']

            for nodo in listadoCanciones:
                if nodo.nombre == cancion_nueva:
                    n = Cancion(nodo.nombre, nodo.artista, nodo.album)
                    colaCanciones.enqueue(n)
                    break
                else:
                    nodo = nodo.next
            start_time = time.time()
            cola_a_Lista()
            print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
            comprobadorQueueTrue(cancion_nueva)
        #se reproduce la primera cancion
        elif 'play' in request.form:
            if cancionActual == " ":
                cancionActual = listadoCanciones.head
                ultimaCancion = cancionActual
            #xCancion = Cancion("Levitating", "Dua Lipa", "Future Nostalgia")
            #colaCanciones.enqueue(xCancion)
            #deletequeue(xCancion.nombre, colaCanciones.head)
        elif 'delete_queue' in request.form:
            cancion_eliminar = request.form['delete_queue']
            cancion = colaCanciones.head
            start_time = time.time()
            deletequeue(cancion_eliminar, cancion)
            print("Time en 'deletequeue': %s  seconds " %(time.time() - start_time))
            start_time = time.time()
            cola_a_Lista()
            print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
        elif 'delete_list' in request.form:
            cancion_eliminar = request.form['delete_list']
            cancion = listadoCanciones.head
            start_time = time.time()
            deletequeue(cancion_eliminar, colaCanciones.head)
            print("Time en 'deletequeue': %s  seconds " %(time.time() - start_time))
            start_time = time.time()
            deletelist(cancion_eliminar, cancion)
            print("Time en 'deletelist': %s  seconds " %(time.time() - start_time))
            start_time = time.time()
            actulizarListaCanciones()
            print("actulizarListaCanciones': %s  seconds " %(time.time() - start_time))
        elif 'añadir_cancion' in request.form:
            nombre_cancion = request.form['cancion']
            artista = request.form['autor']
            album = request.form['album']
            start_time = time.time()
            añadirCancion(nombre_cancion,artista,album)
            print("Time en 'añadirCancion': %s  seconds " %(time.time() - start_time))
            start_time = time.time()
            actulizarListaCanciones()
            print("Time en 'actulizarListaCanciones': %s  seconds " %(time.time() - start_time))
        else:
            pass

        template = env.get_template('spoti.html')
        if(cancionActual != " "):
            return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion=cancionActual.nombre,style_sheet=css )
        else:
            return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion="---",style_sheet=css )
    template = env.get_template('spoti.html')
    return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion="---", style_sheet=css)

if __name__ == '__main__':
    app.run(debug=True)