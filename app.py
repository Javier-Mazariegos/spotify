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
cancionActual = listadoCanciones.head
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


cargarCanciones()
#principal
@app.route('/', methods=["GET","POST"], endpoint='index')
def index():
    global cancionActual, listaCanciones, listadoCanciones, colaCanciones, ultimaCancion
    contador = 0 

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
        #se reproduce la primera cancion
        elif request.form.get('play') == 'play':
            cancionActual = listadoCanciones.head
            ultimaCancion = cancionActual
            #colaCanciones.enqueue(Cancion("Levitating", "Dua Lipa", "Future Nostalgia"))
        else:
            pass
        template = env.get_template('index.html')
        return template.render(listadoCanciones = listaCanciones, nombreCancion=cancionActual.nombre,nombreArtista=cancionActual.artista,nombreAlbum=cancionActual.album )
    template = env.get_template('index.html')
    return template.render(listadoCanciones = listaCanciones, nombreCancion="---",nombreArtista="---",nombreAlbum="---")




@app.route('/añadir', methods=["GET","POST"], endpoint='añadir')
def añadir():
    if(request.method == "POST"):
        nombre = request.form['var1']
        artista = request.form['var2']
        album = request.form['var3']
        añadirCancion(nombre,artista,album)
    template = env.get_template('añadir.html')
    return template.render()


#eliminar cancion y ver si esta en la cola
#agregar a la cola



@app.route('/listar', endpoint='listar')
def listar():
    #limpiarListado()
    #cargarCanciones()
    template = env.get_template('listar.html')
    return template.render(my_list=listadoCanciones.head, indice = indice)





if __name__ == '__main__':
    app.run(debug=True)

#cProfile.run("listadoCanciones.insertar('The Show Must Go On','Queen','Innuendo')")
#cProfile.run("añadirCancion('The Show Must Go On','Queen','Innuendo')")
#cProfile.run("cargarCanciones()")