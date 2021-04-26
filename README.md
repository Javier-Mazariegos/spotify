# Api que permite gestionar una playlist

 ## Problem:
    Manejar de forma eficiente la reproducción de música, tomando en cuenta los aspecto de agregar a la fila, nueva canción, eliminar canción y reproducir canción.
    La importancia de solucionar este problema, es que los reproductores de música consumen muchos recursos. 
  ## Goals:
    El reproductor de música logrará gestionar de una manera eficiente una playlist, en donde pueda reproducir una canción, agregarla a la cola, eliminar y agregar en la lista.
  ## Context:
    El servicio en línea, denominado también como: TortolaPlay, busca mejorar la eficiencia de su reproductor de música para que las personas quieran utilizarlo en vez de spotify, deezer, etc. 
  ## Detailed Solution:
    Se utilizaron las estructuras: Queue, LinkesList, Arrays para poder gestionar una playlist. 
    La API cuenta con una ruta unicamente, en ella se pueden realizar las siguientes acciones: Play, Play next, Play previous, Play canción nueva, Agregar a la cola, Eliminar de la cola, Agregar a la lista y Eliminar de la lista. 
     
    Descripción de acciones:
    Play: Reproduce la primera canción si no se está reproduciendo ninguna.
    Play Next: Reproduce la siguiente canción.
    Play Previous: Reproduce la canción anterior.
    Play canción nueva: Reproduce la canción a la que se le da play.
    Agregar a la cola: Agrega una nueva canción a la cola de reproducción.
    Eliminar de la cola: Elimina una canción de la cola cuando se reproduce o cuando se elimina directamente. 
    Agregar a la lista: Agrega una canción a la base de datos (CSV) y agrega la canción a la linkedlist
    Eliminar de la lista: Elimina una canción de la base de datos (CSV) y la elimina de la linkedlist
  ## Dates:
    Para el día miércoles 21 de abril, aspecto visual terminado y backend por la mitad. 
    Para el día viernes 23 de abril, unión completa entre backend y aspecto visual
    De sábado 24 a domingo 25 de abril, tiempo para unit testing, profiling, video de ejecución y test automatization. 
    Lunes 26 de abril, entrega del proyecto.  
# Diagrama de casos de uso:
   ![image](https://user-images.githubusercontent.com/61554803/116135618-9167d500-a68e-11eb-8512-a4ad795f65eb.png)
   Link: https://lucid.app/lucidchart/invitations/accept/5a2a3726-ce2d-4c1f-881a-db6a1518c77b
# Tiempos de funciones:
   ![image](https://user-images.githubusercontent.com/61555440/116156137-54a8d780-a6a8-11eb-895b-1e907b14d839.png)
# Video de ejecución satisfactoria con Selenium
   
    
