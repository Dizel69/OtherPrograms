import turtle
import random

turtle.hideturtle()
turtle.speed(100)

# Размер точек
dot_size = 6

# Построение равностороннего треугольника
vertices = []
for _ in range(3):
    vertices.append(turtle.pos())
    turtle.forward(500)
    turtle.left(120)

turtle.penup()

# Извлечение координат вершин
coords = [(int(p[0]), int(p[1])) for p in vertices]
x1, y1 = coords[0]
x2, y2 = coords[1]
x3, y3 = coords[2]

# Выбор стартовой точки внутри треугольника
while True:
    px, py = random.randint(x1, x2), random.randint(y2, y3)
    turtle.goto(px, py)
    
    # Проверка на принадлежность точке треугольнику
    def is_inside(x, y):
        b1 = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y) >= 0
        b2 = (x2 - x) * (y3 - y2) - (x3 - x2) * (y2 - y) >= 0
        b3 = (x3 - x) * (y1 - y3) - (x1 - x3) * (y3 - y) >= 0
        return b1 == b2 == b3
    
    if is_inside(px, py):
        turtle.dot(dot_size)
        break

# Генерация точек
for _ in range(10000):
    vx, vy = random.choice(coords)
    px, py = (px + vx) / 2, (py + vy) / 2
    turtle.goto(px, py)
    color = "blue" if (vx, vy) == coords[0] else "red" if (vx, vy) == coords[1] else "green"
    turtle.dot(dot_size, color)

turtle.done()
