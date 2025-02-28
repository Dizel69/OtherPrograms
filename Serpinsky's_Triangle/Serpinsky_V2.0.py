import turtle
import random

# Размер точек
dot_size = 6
vertices = []
start_point = []


def on_click(x, y):
    global vertices, start_point
    if len(vertices) < 3:
        vertices.append((x, y))
        turtle.goto(x, y)
        turtle.dot(dot_size, "black")
        if len(vertices) == 3:
            print("Треугольник задан. Теперь выберите начальную точку внутри него.")
    elif len(start_point) == 0:
        start_point.append((x, y))
        turtle.goto(x, y)
        turtle.dot(dot_size, "purple")
        print("Начальная точка выбрана. Запуск алгоритма...")
        turtle.ontimer(generate_sierpinski, 500)


def generate_sierpinski():
    px, py = start_point[0]

    for _ in range(10000):
        vx, vy = random.choice(vertices)
        px, py = (px + vx) / 2, (py + vy) / 2
        turtle.goto(px, py)
        color = "blue" if (vx, vy) == vertices[0] else "red" if (vx, vy) == vertices[1] else "green"
        turtle.dot(dot_size, color)

    print("Генерация завершена.")


turtle.speed(0)
turtle.hideturtle()
turtle.penup()
print("Кликните три раза для задания вершин треугольника, затем ещё раз для выбора начальной точки.")
turtle.onscreenclick(on_click)
turtle.done()
