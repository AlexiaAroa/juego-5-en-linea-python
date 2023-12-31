import gamelib

ALTO_GRILLA = 10 # Cantidad de celdas de alto que hay en la grilla 
ANCHO_GRILLA = 10 # cantidad de celdas de ancho que hay en la grilla

TAMANIO_CELDA = 30 # Tamaño de la celda en píxeles
DISTANCIA_CELDA = 7 # Distancia de los símbolos ('X', 'O') en píxeles respecto de la celda
INICIO_GRILLA = TAMANIO_CELDA# Pixel en el que inicia la grilla

ALTURA_PIXELES_GRILLA = TAMANIO_CELDA * ALTO_GRILLA # Altura de la grilla en píxeles
ANCHO_PIXELES_GRILLA = TAMANIO_CELDA * ANCHO_GRILLA # Ancho de la grilla en píxeles

FINAL_GRILLA = INICIO_GRILLA + ALTURA_PIXELES_GRILLA  # Pixel en el que termina la grilla

ANCHO_VENTANA = TAMANIO_CELDA * ANCHO_GRILLA # Ancho de la ventana en píxeles
ALTO_VENTANA = INICIO_GRILLA * 2 + ALTURA_PIXELES_GRILLA # Alto de la ventana en píxeles

CRUZ = 'X'
CIRCULO = 'O'
VACIO = ''

def juego_crear():
    """Inicializar el estado del juego: devuelve una grilla vacía y el turno del jugador."""
    return [[VACIO for i in range(ANCHO_GRILLA)] for j in range(ALTO_GRILLA)], CIRCULO

def obtener_coordenadas_matriz(x, y):
    """Recibe coordenadas en píxeles y devuelve coordenadas adaptadas a la matriz."""
    # columna, fila = -1, -1

    # if 1 <= x <= ANCHO_VENTANA - 1 and INICIO_GRILLA + 1 <= y <= FINAL_GRILLA - 1:
    #     if x % TAMANIO_CELDA != 0 and y % TAMANIO_CELDA != 0:
    #         columna, fila = x // TAMANIO_CELDA, (y // TAMANIO_CELDA) - 1
    columna, fila = x // TAMANIO_CELDA, (y // TAMANIO_CELDA) - 1
    columna, fila = x // TAMANIO_CELDA, (y - INICIO_GRILLA) // TAMANIO_CELDA
    return columna, fila

def obtener_coordenadas_pixel(columa, fila):
    """Recibe coordenadas de la matriz y devuelve coordenadas adaptadas en píxeles."""
    # return columa * TAMANIO_CELDA, (fila + 1) * TAMANIO_CELDA # Fijate que la parte de fila sólo funciona si TAMANIO_CELDA == INICIO CELDA!
    return columa * TAMANIO_CELDA, fila * TAMANIO_CELDA + INICIO_GRILLA

def actualizar_turno(jugador):
    """Actualiza el turno del jugador."""
    if jugador == CIRCULO:
        return CRUZ
    return CIRCULO

def movimiento_es_valido(juego, x, y):
    '''Devuelve True si la posición donde se hizo click es una celda vacía de la grilla.'''
    columna, fila = obtener_coordenadas_matriz(x, y)
    return x % TAMANIO_CELDA != 0 and y % TAMANIO_CELDA != 0 and 0 <= columna <= 9 and 0 <= fila <= 9 and juego[fila][columna] == VACIO

def juego_actualizar(juego, x, y):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    grilla, jugador = juego
    if movimiento_es_valido(grilla, x, y):
        columna, fila = obtener_coordenadas_matriz(x, y)
        grilla[fila][columna], jugador = jugador, actualizar_turno(jugador)
    
    return grilla, jugador

def dibujar_cruz(x1, y1):
    """Dibuja una cruz en la celda donde el usuario hizo click."""
    gamelib.draw_line(x1 + DISTANCIA_CELDA, y1 + DISTANCIA_CELDA, x1 + TAMANIO_CELDA - DISTANCIA_CELDA, y1 + TAMANIO_CELDA - DISTANCIA_CELDA, fill='white', width=1) 
    gamelib.draw_line(x1 + DISTANCIA_CELDA, y1 + TAMANIO_CELDA - DISTANCIA_CELDA, x1 + TAMANIO_CELDA - DISTANCIA_CELDA, y1 + DISTANCIA_CELDA, fill='white', width=1)

def dibujar_circulo(x1, y1):
    """Dibuja un círculo en la celda donde el usuario hizo click."""
    gamelib.draw_oval(x1 + DISTANCIA_CELDA, y1 + DISTANCIA_CELDA, x1 + TAMANIO_CELDA - DISTANCIA_CELDA, y1 + TAMANIO_CELDA - DISTANCIA_CELDA, outline='white', fill='black')

def dibujar_grilla():
    """Dibuja la grilla del juego."""
    #Líneas verticales
    for i in range(0, ANCHO_PIXELES_GRILLA + 1, TAMANIO_CELDA):
        gamelib.draw_line(i, INICIO_GRILLA, i, FINAL_GRILLA, fill='white', width=1)

    #Líneas horizontales
    for i in range(INICIO_GRILLA, FINAL_GRILLA + 1, TAMANIO_CELDA):
        gamelib.draw_line(0, i, ANCHO_VENTANA, i, fill='white', width=1)

def juego_mostrar(juego):
    """Actualizar la ventana."""
    grilla, jugador = juego
    gamelib.draw_text('5 en línea', ANCHO_VENTANA // 2, INICIO_GRILLA // 2)
    gamelib.draw_text(f'Turno: {jugador}', ANCHO_VENTANA // 2, (FINAL_GRILLA + ALTO_VENTANA) // 2)
    dibujar_grilla()

    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if grilla[i][j] == CRUZ:
                x, y = obtener_coordenadas_pixel(j, i)
                dibujar_cruz(x, y)

            if grilla[i][j] == CIRCULO:
                x, y = obtener_coordenadas_pixel(j, i)
                dibujar_circulo(x, y)

def main():
    juego = juego_crear()

    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego = juego_actualizar(juego, x, y)

gamelib.init(main)
