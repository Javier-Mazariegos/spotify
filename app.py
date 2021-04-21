from memory_profiler import profile
from flask import Flask, request
from jinja2 import Template, Environment, FileSystemLoader
import csv
import cProfile
from linkedlist import Cancion, LinkedList

listadoCanciones = LinkedList()
listaCanciones = []
indice = listadoCanciones.head
cargarCanciones()
cancionActual = listadoCanciones.head

File_loader = FileSystemLoader("templates")
env = Environment(loader=File_loader)
app = Flask(__name__)



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
    global listadoCanciones
    with open('listado.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            datos = row
            #if contador == 0:
            #    listadoCanciones.push(datos[0],datos[1],datos[2])
            #else:
            listaCanciones.append(Cancion(datos[0],datos[1],datos[2]))
            listadoCanciones.insertar(datos[0],datos[1],datos[2])


#principal
@app.route('/', methods=["GET","POST"], endpoint='index')
def index():
    global cancionActual, listaCanciones, listadoCanciones
    contador = 0 

    #cambiar cancion
    if(request.method == "POST"):
        if request.form.get('Play Previous') == 'Play Previous':
            if(cancionActual.previous is None):
                pass
            else:
                cancionActual = cancionActual.previous
        elif request.form.get('Play Next') == 'Play Next':
            if(cancionActual.next is None):
                pass
            else:
                cancionActual = cancionActual.next
        elif request.form.get('play nueva') == 'play nueva':
            cancion_nueva = request.form.get('nombre cancion')
            if cancionActual != cancion_nueva:    
                cancion = listadoCanciones.head
                while (True):
                    if cancion.next is not None:
                        if cancion_nueva == cancion.nombre:
                            cancionActual = cancion
                            break    
                    else:
                        break
            else:
                pass

        else:
            pass
        template = env.get_template('index.html')
        return template.render(nombreCancion=cancionActual.nombre,nombreArtista=cancionActual.artista,nombreAlbum=cancionActual.album )

    

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




@app.route('/listar', endpoint='listar')
def listar():
    #limpiarListado()
    #cargarCanciones()
    template = env.get_template('listar.html')
    return template.render(my_list=listadoCanciones.head, indice = indice)

if __name__ == '__main__':
    app.run()

cProfile.run("listadoCanciones.insertar('The Show Must Go On','Queen','Innuendo')")
cProfile.run("añadirCancion('The Show Must Go On','Queen','Innuendo')")
cProfile.run("cargarCanciones()")