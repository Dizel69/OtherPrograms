#импорт черепахи и рандома
import random
from turtle import *

list_triangle = []

ht()
#скорость 100 - максимальная, да медленно
speed(100)
#это переменная, отвечающая за размер точек
size_point = 6

#создание равностороннего треугольника
for i in range(3):
    list_triangle.append(pos())
    fd(500)
    lt(120)

up()

#взятие координат вершин
x1 = int(float(str(list_triangle[0]).replace(")", "").replace("(", "").split(",")[0]))
x2 = int(float(str(list_triangle[1]).replace(")", "").replace("(", "").split(",")[0]))
x3 = int(float(str(list_triangle[2]).replace(")", "").replace("(", "").split(",")[0]))
y1 = int(float(str(list_triangle[0]).replace(")", "").replace("(", "").split(",")[1]))
y2 = int(float(str(list_triangle[1]).replace(")", "").replace("(", "").split(",")[1]))
y3 = int(float(str(list_triangle[2]).replace(")", "").replace("(", "").split(",")[1]))

#постановка точки в случайном месте и проверка на нахождение точки внутри треугольника
while True:
    point_x = random.randint(x1,x2)
    point_y = random.randint(y2,y3)
    goto(point_x, point_y)
    if (x1 - point_x) * (y2 - y1) - (x2 - x1) * (y1 - point_y) >= 0 and \
            (x2 - point_x) * (y3 - y2) - (x3 - x2) * (y2 - point_y) >= 0 and \
            (x3 - point_x) * (y1 - y3) - (x1 - x3) * (y3 - point_y) >= 0:
        dot(size=size_point)
        break
    elif (x1 - point_x) * (y2 - y1) - (x2 - x1) * (y1 - point_y) < 0 and \
            (x2 - point_x) * (y3 - y2) - (x3 - x2) * (y2 - point_y) < 0 and \
            (x3 - point_x) * (y1 - y3) - (x1 - x3) * (y3 - point_y) < 0:
        dot(size=size_point)
        break
    else:
        pass

#постановка точки в середине отрезка между данной и рандомной вершиной
for k in range(10000):  #в range указано нужное кол-во точек
    top_triangle = random.randint(1,3)
    if top_triangle == 1:
        goto((x1 + point_x)/2, (y1 + point_y)/2)
        dot(size_point, "blue")
        point_x = xcor()
        point_y = ycor()
    elif top_triangle == 2:
        goto((x2 + point_x)/2, (y2 + point_y)/2)
        dot(size_point, "red")
        point_x = xcor()
        point_y = ycor()
    else:
        goto((x3 + point_x)/2, (y3 + point_y)/2)
        dot(size_point, "green")
        point_x = xcor()
        point_y = ycor()