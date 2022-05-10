"""Pacman, classic arcade game.

Autores:
Programador 1: Moisés Adame Aguilar         (A01660927)
Programador 2: Ricardo Campos Luna          (A01656898)
Programador 3: Humberto Ivan Ulloa Cardona  (A01657143)

Fecha: 10 de Mayo del 2022
"""

from random import choice, randint
from turtle import *

from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)

# Se agregan las posibles combinaciones de colores para el tablero y se elige  una
colors = {'#0a0a0a': '#0909e0', '#460578': '#f36cf5', '#0c6b03': '#e09eff'}
color_index = randint(0, len(colors))
color_bg = list(colors.keys())[color_index]
color_path = list(colors.values())[color_index]

ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor(color_bg)
    path.color(color_path)

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    # Se estableció la fuente a Arial del 30 pts en itálica
    writer.undo()
    style = ('Arial', 30, 'italic')
    writer.write(state['score'], font=style, align='center')

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')
    
    for point, course in ghosts:
        # Saber donde esta pacman con respecto del fantasma
            """Aqui se busca la posicion del pacmam y se compara con la del fantasma para que este prefiera la moverse a donde esta el pacman cuando lo puede ver"""
        
            if pacman.x < point.x and pacman.y == point.y: # Si el pacman esta exactamente a la izquierda
                options = [vector(-10,0), vector(0,-10), vector(10,0), vector(0,10)]
            elif pacman.x > point.x and pacman.y == point.y: # Si el pacman esta exactamente a la derecha
                options = [vector(10, 0), vector(0,-10), vector(-10,0), vector(0,10)]
            elif pacman.y < point.y and pacman.x == point.x: # Si el pacman esta exactamente abajo
                options = [vector(0,-10), vector(-10,0), vector(10,0), vector(0,10)]
            elif pacman.y > point.y and pacman.x == point.x: # Si el pacman esta exactamente arriba
                options = [vector(0,10), vector(10, 0), vector(0,-10), vector(-10,0)]

            elif pacman.y < point.y and pacman.x < point.x: # Si el pacman esta abajo a la izquierda
                if abs(pacman.y - point.y) > abs(pacman.x - point.x): # Mas abajo que a la izquierda
                    options = [vector(0,-10), vector(-10,0), vector(10,0), vector(0,10)]    
                else:
                    options = [vector(-10,0), vector(0,-10), vector(10,0), vector(0,10)]
                    
            elif pacman.y > point.y and pacman.x < point.x: # Si el pacman esta arriba a la izquierda
                if abs(pacman.y - point.y) > abs(pacman.x - point.x): # Mas arriba que hacia la izquierda
                    options = [vector(10,0), vector(-10,0), vector(0,10), vector(0,-10)]
                else:
                    options = [vector(0, 10), vector(-10, 0), vector(10,0), vector(0,-10)]


            elif pacman.y < point.y and pacman.x > point.x: # Si el pacman esta abajo a la derecha
                if abs(pacman.y - point.y) > abs(pacman.x - point.x): # Mas hacia abajo que hacia la derecha
                    options = [vector(0, -10),vector(10, 0), vector(-10,0), vector(0, 10)]
                else:
                    options = [vector(10, 0), vector(0, -10), vector(-10,0), vector(0, 10)]


            elif pacman.y > point.y and pacman.x > point.x:  # Si el pacman esta hacia arriba a la derecha
                if abs(pacman.y - point.y) > abs(pacman.x - point.x): # Mas arriba que hacia la derecha
                    options = [vector(0, 10), vector(10,0), vector(-10, 0),vector(0,-10)]
                else:
                    options = [vector(10,0), vector(0, 10), vector(0,-10), vector(-10, 0)]


            else:
                options = [vector(10,0),vector(-10,0),vector(0,10),vector(0,-10)]
        
            possible_options = valid_options(point)

            for movimiento in options:
                if movimiento in possible_options:
                    plan = movimiento
                    break

            course.x = plan.x
            course.y = plan.y
            point.move(course)

            up()
            goto(point.x + 10, point.y + 10)
            dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    # Se disminuyó el timepo entre cada frame para aumentar la velocidad 
    # de los fantasmas.
    ontimer(move, 25)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

def valid_options(point):
    "Return the valid directions for ghosts given the position"
    options = [vector(10,0), vector(-10,0), vector(0,10), vector(0,-10)]
    optionsv = []

    for i in options:
        if valid(point + i):
            optionsv.append(i)
        
    return optionsv



setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()



