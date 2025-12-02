#rumus brensenhem
def draw_line(x1,y1,x2,y2):
    points = []
    dx=abs(x2-x1)
    dy=abs(y2-y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points


def draw_polygon(vertices):
    all_points=[]
    n=len(vertices)
    for i in range(n):
        x1,y1 = vertices[i]
        x2,y2 = vertices[(i+1)%n]
        all_points.extend(draw_line(x1,y1,x2,y2))
    return all_points

#tambahkan bgian ini
import turtle

def draw_points(points):
    turtle.speed(0)
    turtle.penup()
    for x,y in points:
        turtle.goto(x*20, y*20) #skala agar terlihat
        turtle.dot(5,'black')
    turtle.done()
    
#contoh persegi
vertices=[(2,2),(6,2),(6,6),(2,6)]
points = draw_polygon(vertices)
draw_points(points)