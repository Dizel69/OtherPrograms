import turtle

print("Насколько большой фрактал вы хотите от 1 до 7?")
deep = int(input())

if(deep == 0 or deep > 7):
    print("Введите число от 1 до 7")

def drawTriangle(points, color, myTurtle):
    myTurtle.fillcolor(color)
    myTurtle.up()
    myTurtle.goto(points[0][0], points[0][1])
    myTurtle.down()
    myTurtle.begin_fill()
    myTurtle.goto(points[1][0], points[1][1])
    myTurtle.goto(points[2][0], points[2][1])
    myTurtle.goto(points[0][0], points[0][1])
    myTurtle.end_fill()
def getMid(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
def Serpinsky(points, degree, myTurtle):
    colormap = ['black', 'purple', 'green', 'white', 'yellow', 'violet', 'orange', 'red']
    drawTriangle(points, colormap[degree], myTurtle)
    if degree > 0:
        Serpinsky([points[0],
                    getMid(points[0], points[1]),
                    getMid(points[0], points[2])],
                   degree-1, myTurtle)
        Serpinsky([points[1],
                    getMid(points[0], points[1]),
                    getMid(points[1], points[2])],
                   degree-1, myTurtle)
        Serpinsky([points[2],
                    getMid(points[2], points[1]),
                    getMid(points[0], points[2])],
                   degree-1, myTurtle)

myTurtle = turtle.Turtle()
myWin = turtle.Screen()
myPoints = [[-100, -50], [0, 100], [100, -50]]
Serpinsky(myPoints, deep, myTurtle)
myWin.exitonclick()
