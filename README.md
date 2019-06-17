# Ripv1-Simulation


# Descripción:
Para el proyecto de laboratorio, se debe programar una simulación de enrutamiento RIP, conforme a la topología adjunta.

# Restricciones:
    • El protocolo de transporte a utilizar es UDP.
    • Debe crear un programa que sea capaz de simular el envío de paquetes de RIP, así como de recibirlos y actualizar las tablas de rutas utilizando las reglas que RIP establece para ello.
    • Debe implementar “Split horizon” (no propagar una ruta a través de la interfaz por la cual se aprendió).
    • Al ejecutar el programa, se debe digitar el número de nodo que representa la ejecución de este proceso (en total, se simulan 5 nodos, según diagrama adjunto).
    • No es necesario simular los enlaces de comunicación entre routers.
    • El programa debe funcionar en el mismo equipo, o bien en equipos diferentes, y comunicarse utilizando “sockets”.  La comunicación se realizará mediante “broadcast” o “multicast” (debe investigar cómo realizar esto), pero debe descartar mensajes recibidos de nodos que no son vecinos.  El puerto destino puede ser fijo (hard-coded).
    • Las actualizaciones de tablas de rutas se enviarán cada 10 segundos. 
    • Después de un minuto de ejecución, el nodo 3 debe finalizar la ejecución, y con ello se deben actualizar las tablas de rutas adecuadamente utilizando los mecanismos de distancia infinita, poison reverse y hold timer (20 segundos)
    • Debe poder visualizar en cada nodo la evolución de las tablas de rutas.
