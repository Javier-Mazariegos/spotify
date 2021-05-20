from flask.helpers import url_for
from memory_profiler import profile
from flask import Flask, request, redirect
from jinja2 import Template, Environment, FileSystemLoader
import csv
import time
from linkedlist import Cancion, LinkedList
from queue import Queue
from sh1 import SHA1Hash
import argparse
from graph import Graph
from graphviz import Digraph


File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)

dot = Digraph(comment='The Round Table')
G2 = Graph()
listadoCanciones = LinkedList()
colaCanciones = Queue()
listaCanciones = []
colaLista = []
cancionActual = " "
ultimaCancion = None
buscador_canciones = {}
ENCONTRADA = False
find = None
def comprimir(n: str):
    n = n.lower()
    n = n.replace(" ", "")
    return n
@profile
def añadirCancion(nombre,artista,album)-> None:
    global listadoCanciones, buscador_canciones
    datos = ["","",""]
    datos[0] = nombre
    datos[1] = artista
    datos[2] = album
    with open('listado.csv','a',newline='') as writeFile:
        writer = csv.writer(writeFile,delimiter=",",quotechar=',',quoting=csv.QUOTE_MINIMAL,lineterminator='')
        writer.writerow('\n')
        writer.writerow(datos)
    #listaCanciones.append(Cancion(datos[0],datos[1],datos[2]))
    can = Cancion(datos[0],datos[1],datos[2])
    listadoCanciones.insertar(can)
    nombrehash = comprimir(nombre)
    parser = argparse.ArgumentParser(description="Process some strings or files")
    parser.add_argument(
        "--string",
        dest="input_string",
        default=nombrehash,
        help="Hash the string",
    )
    args = parser.parse_args()
    input_string = args.input_string
    hash_input = bytes(input_string, "utf-8")
    hash_var = (SHA1Hash(hash_input).final_hash())
    buscador_canciones[hash_var] = listadoCanciones.last()
    comprobadorListadoTrue(datos[0])

def contadorListado(nombreCancion):
    global listadoCanciones
    comprobacion = False
    for c in listadoCanciones:
        if nombreCancion == c.nombre:
            comprobacion = True
            break
    return comprobacion

def contadorQueue(nombreCancion):
    comprobacion = False
    entrada = colaCanciones.is_empty1()
    currentNode = colaCanciones.head

    if entrada == False:
        
        if nombreCancion == currentNode.nombre:
            comprobacion = True
            entrada = True

        while (True):
            if entrada == False:
                if nombreCancion == currentNode.nombre:
                    comprobacion = True
                    break
                if currentNode.next is not None:
                    currentNode = currentNode.next
                else:
                    break
            else:
                break
    return comprobacion
 

def comprobadorListadoTrue(nombreCancion):
    resultado = contadorListado(nombreCancion)
    assert resultado == True, "Debe ser True"

def comprobadorListadoFalse(nombreCancion):
    resultado = contadorListado(nombreCancion)
    assert resultado == False, "Debe ser False"
    
def comprobadorQueueTrue(nombreCancion):
    resultado = contadorQueue(nombreCancion)
    assert resultado == True, "Debe ser True"

def comprobadorQueueFalse(nombreCancion):
    resultado = contadorQueue(nombreCancion)
    assert resultado == False, "Debe ser False"


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
    global listadoCanciones, listaCanciones, buscador_canciones
    with open('listado.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            datos = row
            #if contador == 0:
            #    listadoCanciones.push(datos[0],datos[1],datos[2])
            #else:
            can = Cancion(datos[0],datos[1],datos[2])
            listaCanciones.append(can)
            listadoCanciones.insertar(can)
            nombrehash = comprimir(can.nombre)
            parser = argparse.ArgumentParser(description="Process some strings or files")
            parser.add_argument(
                "--string",
                dest="input_string",
                default=nombrehash,
                help="Hash the string",
            )
            args = parser.parse_args()
            input_string = args.input_string
            hash_input = bytes(input_string, "utf-8")
            hash_var = (SHA1Hash(hash_input).final_hash())
            buscador_canciones[hash_var] = listadoCanciones.last()
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
    global listadoCanciones, buscador_canciones
    nombrehash = comprimir(cancion_eliminar)
    parser = argparse.ArgumentParser(description="Process some strings or files")
    parser.add_argument(
        "--string",
        dest="input_string",
        default=nombrehash,
        help="Hash the string",
    )
    args = parser.parse_args()
    input_string = args.input_string
    hash_input = bytes(input_string, "utf-8")
    hash_var = (SHA1Hash(hash_input).final_hash())
    buscador_canciones.pop(hash_var)
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
    start_time = time.time()
    eliminarCancion()
    print("Time en 'eliminarCancion': %s  seconds " %(time.time() - start_time))
    comprobadorListadoFalse(cancion_eliminar)


#principal
@app.route('/', methods=["GET","POST"], endpoint='index')
@profile
def index():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista, ENCONTRADA, find
    contador = 0 
    css = url_for('static', filename='micss.css')
    imgF = url_for('static', filename='Diagrama de Grafo .png')
    template = env.get_template('spoti.html')
    print("entre al index")
    if(cancionActual != " "):
        return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion=cancionActual.nombre,style_sheet=css, r = ENCONTRADA, find = find, foto = imgF)
    else:
        return template.render(colaLista = colaLista, listadoCanciones = listaCanciones, nombreCancion="---",style_sheet=css, r=ENCONTRADA, find = find, foto = imgF)

@app.route('/Play_Previous', methods=["GET","POST"]) #<-- Ruta para cambiar a la cancion anterior
def Play_Previous():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if(request.method == "POST"):
        if 'Play_Previous' in request.form:
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
    return redirect(url_for('index'), 301)

@app.route('/Play_Next', methods=["GET","POST"]) #<-- Ruta para cambiar a la siguiente cancion
def Play_Next():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if'Play_Next' in request.form:
        if colaCanciones.is_empty1() == True:
            if ultimaCancion != None:
                if( ultimaCancion.next == listadoCanciones.head or ultimaCancion.next is None):
                    cancionActual = listadoCanciones.head
                    ultimaCancion = cancionActual
                else:
                    cancionActual = ultimaCancion.next
                    ultimaCancion = cancionActual
            else:
                cancionActual = listadoCanciones.head
                ultimaCancion = cancionActual
        else:
            cancionActual = colaCanciones.dequeue()
        start_time = time.time()
        cola_a_Lista()
        print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/play_nueva', methods=["GET","POST"]) #<-- Ruta para reproducir una cancion especifica
def play_nueva():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'play_nueva' in request.form:
        cancion_nueva = request.form['play_nueva']
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
    return redirect(url_for('index'), 301)

@app.route('/agregar', methods=["GET","POST"]) #<-- Ruta para agregar una cancion a la cola
def agregar():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'agregar' in request.form:
        cancion_nueva = request.form['agregar']
        for nodo in listadoCanciones:
            if nodo.nombre == cancion_nueva:
                n = Cancion(nodo.nombre, nodo.artista, nodo.album)
                colaCanciones.enqueue(n)
                comprobadorQueueTrue(cancion_nueva)
                break
            else:
                nodo = nodo.next
        start_time = time.time()
        cola_a_Lista()
        print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/play', methods=["GET","POST"]) #<-- Ruta para reproducir la primera cancion de la lista
def play():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'play' in request.form:
        if cancionActual == " ":
            cancionActual = listadoCanciones.head
            ultimaCancion = cancionActual
    return redirect(url_for('index'), 301)

@app.route('/delete_queue', methods=["GET","POST"]) #<-- Ruta para eliminar de la cola
def delete_queue():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'delete_queue' in request.form:
        cancion_eliminar = request.form['delete_queue']
        cancion = colaCanciones.head
        start_time = time.time()
        deletequeue(cancion_eliminar, cancion)
        print("Time en 'deletequeue': %s  seconds " %(time.time() - start_time))
        start_time = time.time()
        cola_a_Lista()
        print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/delete_list', methods=["GET","POST"]) #<-- Ruta para eliminar de la lista
def delete_list():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'delete_list' in request.form:
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
    return redirect(url_for('index'), 301)

@app.route('/añadir_cancion', methods=["GET","POST"]) #<-- Ruta para añadir una nueva cancion al CSV
def añadir_cancion():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    if 'añadir_cancion' in request.form:
        nombre_cancion = request.form['cancion']
        artista = request.form['autor']
        album = request.form['album']
        start_time = time.time()
        añadirCancion(nombre_cancion,artista,album)
        print("Time en 'añadirCancion': %s  seconds " %(time.time() - start_time))
        start_time = time.time()
        actulizarListaCanciones()
        print("Time en 'actulizarListaCanciones': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/buscar_cancion', methods=["GET","POST"]) #<-- Ruta para buscar una cancion
def buscar_cancion():
    global ENCONTRADA
    if 'buscar_cancion' in request.form:
        nombre_cancion = request.form['cancion_buscar']
        nombre_cancion = comprimir(nombre_cancion)
        #print(nombre_cancion)
        parser = argparse.ArgumentParser(description="Process some strings or files")
        parser.add_argument(
            "--string",
            dest="input_string",
            default=nombre_cancion,
            help="Hash the string",
        )
        args = parser.parse_args()
        input_string = args.input_string
        hash_input = bytes(input_string, "utf-8")
        hash_var = (SHA1Hash(hash_input).final_hash())
        global buscador_canciones, find
        if buscador_canciones.get(hash_var) is not None:
            ENCONTRADA = True
            find = buscador_canciones[hash_var]
        else:
            ENCONTRADA = False
            find = None
    return redirect(url_for('index'), 301)

# <=========================================== Rutas para hacer pruebas en jmeter ================================================================>


@app.route('/play_nueva_Test/<test_cancion>', methods=["GET","POST"]) #<-- Ruta para reproducir una cancion especifica
def play_nueva_Test(test_cancion = None):
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    cancion_nueva = test_cancion
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
    return redirect(url_for('index'), 301)

@app.route('/agregar_Test/<test_cancion>', methods=["GET","POST"]) #<-- Ruta para agregar una cancion a la cola
def agregar_Test(test_cancion = None):
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    cancion_nueva = test_cancion
    for nodo in listadoCanciones:
        if nodo.nombre == cancion_nueva:
            n = Cancion(nodo.nombre, nodo.artista, nodo.album)
            colaCanciones.enqueue(n)
            comprobadorQueueTrue(cancion_nueva)
            break
        else:
            nodo = nodo.next
    start_time = time.time()
    cola_a_Lista()
    print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/delete_queue_Test/<test_cancion>', methods=["GET","POST"]) #<-- Ruta para eliminar de la cola
def delete_queue_Test(test_cancion = None):
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    cancion_eliminar = test_cancion
    cancion = colaCanciones.head
    start_time = time.time()
    deletequeue(cancion_eliminar, cancion)
    print("Time en 'deletequeue': %s  seconds " %(time.time() - start_time))
    start_time = time.time()
    cola_a_Lista()
    print("Time en 'cola_a_lista': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/delete_list_Test/<test_cancion>', methods=["GET","POST"]) #<-- Ruta para eliminar de la lista

def delete_list_Test(test_cancion = None):
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    cancion_eliminar =test_cancion
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
    return redirect(url_for('index'), 301)

@app.route('/añadir_cancion_Test/<test_cancion_nombre>/<test_cancion_autor>/<test_cancion_album>', methods=["GET","POST"]) #<-- Ruta para añadir una nueva cancion al CSV

def añadir_cancion_Test(test_cancion_nombre = None,test_cancion_autor = None,test_cancion_album = None):
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion, colaLista
    nombre_cancion = test_cancion_nombre
    artista = test_cancion_autor
    album = test_cancion_album
    start_time = time.time()
    añadirCancion(nombre_cancion,artista,album)
    print("Time en 'añadirCancion': %s  seconds " %(time.time() - start_time))
    start_time = time.time()
    actulizarListaCanciones()
    print("Time en 'actulizarListaCanciones': %s  seconds " %(time.time() - start_time))
    return redirect(url_for('index'), 301)

@app.route('/buscar_cancion/<nombre>', methods=["GET","POST"]) #<-- Ruta para buscar una cancion
def buscar_cancion_Test(nombre = None):
    global ENCONTRADA
    nombre_cancion = nombre
    start_time = time.time()
    nombre_cancion = comprimir(nombre_cancion)
    print("Time en 'comprimir': %s  seconds " %(time.time() - start_time))
    #print(nombre_cancion)
    parser = argparse.ArgumentParser(description="Process some strings or files")
    parser.add_argument(
        "--string",
        dest="input_string",
        default=nombre_cancion,
        help="Hash the string",
    )
    args = parser.parse_args()
    input_string = args.input_string
    hash_input = bytes(input_string, "utf-8")
    start_time = time.time()
    hash_var = (SHA1Hash(hash_input).final_hash())
    print("Time en 'SHA1Hash.final_hash()': %s  seconds " %(time.time() - start_time))
    global buscador_canciones, find
    if buscador_canciones.get(hash_var) is not None:
        ENCONTRADA = True
        find = buscador_canciones[hash_var]
    else:
        ENCONTRADA = False
        find = None
    return redirect(url_for('index'), 301)

if __name__ == '__main__':
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H","I", "J","K", "L", "M", "N", "O","P"]
    edges = [("A", "I"), 
            ("A", "E"),
            ("B", "P"),
            ("B", "J"),
            ("B", "F"),
            ("C", "D"),
            ("C", "G"),
            ("C", "H"),
            ("D", "C"),
            ("D", "G"),
            ("D", "H"),
            ("E", "I"),
            ("E", "P"),
            ("E", "B"),
            ("E", "A"),
            ("F", "K"),
            ("F", "L"),
            ("G", "C"),
            ("G", "D"),
            ("G", "O"),
            ("G", "N"),
            ("H", "K"),
            ("H", "L"),
            ("I", "E"),
            ("I", "P"),
            ("I", "P"),
            ("J", "K"),
            ("J", "L"),
            ("K", "L"),
            ("K", "D"),
            ("L", "D"),
            ("L", "C"),
            ("L", "G"),
            ("L", "N"),
            ("M", "K"),
            ("M", "A"),
            ("N", "M"),
            ("N", "A"),
            ("N", "O"),
            ("N", "G"),
            ("N", "C"),
            ("N", "L"),
            ("O", "N"),
            ("O", "M"),
            ("O", "A"), 
            ("P", "J"),
            ("P", "E"),
            ("P", "I"),
            ("P", "B")
            ]

    for node in nodes:
        G2.add_node(node)
        dot.node(node,node)

    for edge in edges:
        G2.add_edge(edge[0], edge[1])
        dot.edge(edge[0],edge[1])
    #dot.render('./test-output/round-table.gv.pdf', view=True)
    #buscar_cancion()
    start_time = time.time()
    cargarCanciones()
    print("Time en 'cargarCanciones': %s  seconds " %(time.time() - start_time))
    #====================Pruebas del buscador============================================
    #iniciar_arreglo()
    #guardar_en_Array("sdfsdf1sdfdsfdsf1",Cancion("Ejemplo1","ArtistaEjemplo","AlbumEjemplo"))
    #guardar_en_Array("sdfsdf1sdfdsfdsf2",Cancion("Ejemplo1","ArtistaEjemplo","AlbumEjemplo"))
    #print(buscador_canciones[12].nombre)
    #guardar_en_Array("sdfsdf1sdfdsfdsf2",Cancion("Ejemplo2","ArtistaEjemplo","AlbumEjemplo"))
    #print(buscador_canciones[12])
    #guardar_en_Array("sdfsdf1sdfdsfdsf2",Cancion("Ejemplo3","ArtistaEjemplo","AlbumEjemplo"))
    #print(buscador_canciones[12])
    #print("Resultados del buscador")
    #print(buscar_en_Array("sdfsdf1sdfdsfdsf1", "Ejj3"))
    app.run(debug=True)
