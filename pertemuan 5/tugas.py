import turtle

turtle.speed(0)
turtle.hideturtle() #untuk adanya penunjuk dalam pembuatan

#____________________________________________________________________________
#Rumus
#====================
#1. Garis (Bresenham
#====================
def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
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

def draw_points_line(points, offset_x=0, offset_y=0, scale=5):
    turtle.penup()
    for x, y in points:
        turtle.goto(offset_x + x * scale, offset_y + y * scale)
        #turtle.dot(5, "black") #untuk membuat secara titik
        turtle.pendown() #membuat secara garis halus


#====================
#2. Lingkaran
#====================
def midpoint_circle(r):
    x = 0
    y = r
    p = 1 - r
    points = []

    while x <= y:
        points.extend([
            (x, y), (y, x), (-x, y), (-y, x),
            (x, -y), (y, -x), (-x, -y), (-y, -x)
        ])
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1
    return points

def draw_points_circle(points, offset_x=0, offset_y=0, scale=3):
    turtle.penup()
    for x, y in points:
        turtle.goto(offset_x + x * scale, offset_y + y * scale)
        turtle.dot(4, "black")
        

#====================
#3. Poligon
#====================
    #rumus untuk garis, di no 1
def polygon(vertices):
    all_points = []
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        all_points.extend(bresenham_line(x1, y1, x2, y2))
    return all_points


def draw_polygon_points(points, offset_x=0, offset_y=0, scale=5):
    turtle.penup()
    for x, y in points:
        turtle.goto(offset_x + x * scale, offset_y + y * scale)
        #turtle.dot(5, "black")
        turtle.pendown()
    
#____________________________________________________________________________
#-----------------------------------
# Posisi Titik Pusat Gambar
#-----------------------------------
posisi_kiri = (-400,150) # x,y / horizontal,vertical
posisi_tengah = (0,150)
posisi_kanan = (400,150)
Label_y = 230  # teks berada 120px di atas pusat

#____________________________________________________________________________
#================
# 	   Label
#================
#--------------------
# 1. Garis
#--------------------
turtle.penup()
turtle.goto(posisi_kiri[0],Label_y)
turtle.write("Garis (Bresenham)", align="center", font=("Arial", 12, "bold"))
#--------------------
# 2. Lingkaran
#--------------------
turtle.penup()
turtle.goto(posisi_tengah[0],Label_y)
turtle.write("Lingkaran (Midpoint)", align="center", font=("Arial", 12, "bold"))
#--------------------
# 3. Poligon
#--------------------
turtle.penup()
turtle.goto(posisi_kanan[0],Label_y)
turtle.write("Poligon (Bresenham)", align="center", font=("Arial", 12, "bold"))    
    
#____________________________________________________________________________
#===================================        
# 		Menggambar bentuknya        
#=================================== 
#============
# 1.Garis
#============
line_points = bresenham_line(0, 0, 10, 0)
draw_points_line(line_points, posisi_kiri[0], posisi_kiri[1],scale=10)

#============
# 2.Lingkaran
#============
circle_points = midpoint_circle(15)
draw_points_circle(circle_points, posisi_tengah[0], posisi_tengah[1],scale=2)

#============
# 3.Poligon
#============
# bentuk poligon contoh (persegi)
poly_vertices = [
    (0, 0),
    (10, 0),
    (10, 10),
    (0, 10)
    ]
poly_points = polygon(poly_vertices)
draw_polygon_points(poly_points, posisi_kanan[0], posisi_kanan[1])


turtle.done()

