import turtle
import math
import random

# =========================
# SETUP LAYAR
# =========================
screen = turtle.Screen()
screen.setup(1200, 700) #x,y
screen.title("Mini Scene Rumah 2D - Grafika Komputer")
screen.bgcolor("skyblue")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.width(2)

car_pen = turtle.Turtle()
car_pen.hideturtle()
car_pen.speed(0)

tree_pen = turtle.Turtle()
tree_pen.hideturtle()
tree_pen.speed(0)

windmill_pen = turtle.Turtle()
windmill_pen.hideturtle()
windmill_pen.speed(0)

butterfly_pen = turtle.Turtle()
butterfly_pen.hideturtle()
butterfly_pen.speed(0)

# =========================
# 1. ALGORITMA DDA LINE
# =========================
def dda_line(x1, y1, x2, y2, color="black"):
    """Algoritma DDA untuk menggambar garis"""
    pen.color(color)
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        x += x_inc
        y += y_inc
        pen.goto(x, y)
    pen.penup()

# =========================
# 2. ALGORITMA MIDPOINT CIRCLE
# =========================
def lingkaran_isi_midpoint(cx, cy, r, warna="lightblue"):
    """Algoritma Midpoint Circle untuk lingkaran terisi"""
    pen.penup()
    for y in range(-r, r):
        x = int(math.sqrt(r*r - y*y))
        pen.goto(cx - x, cy + y)
        pen.pendown()
        pen.color(warna)
        pen.goto(cx + x, cy + y)
        pen.penup()

# =========================
# 3. ALGORITMA POLYGON
# =========================
def polygon_fill(points, color="green"):
    """Algoritma Scanline untuk mengisi poligon"""
    if len(points) < 3:
        return
    
    min_y = int(min(p[1] for p in points))
    max_y = int(max(p[1] for p in points))
    
    tree_pen.color(color)
    
    for y in range(min_y, max_y + 1):
        intersections = []
        
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            
            y1, y2 = p1[1], p2[1]
            x1, x2 = p1[0], p2[0]
            
            if y1 == y2:
                continue
            
            if min(y1, y2) <= y < max(y1, y2):
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(x_intersect)
        
        intersections.sort()
        
        for i in range(0, len(intersections) - 1, 2):
            if i + 1 < len(intersections):
                tree_pen.penup()
                tree_pen.goto(intersections[i], y)
                tree_pen.pendown()
                tree_pen.goto(intersections[i + 1], y)
    
    tree_pen.penup()

# =========================
# 4. TRANSFORMASI GEOMETRIS 2D
# =========================
def rotate_point(x, y, cx, cy, angle):
    """Transformasi Rotasi"""
    rad = math.radians(angle)
    x -= cx
    y -= cy
    xr = x*math.cos(rad) - y*math.sin(rad)
    yr = x*math.sin(rad) + y*math.cos(rad)
    return xr + cx, yr + cy

def scale_point(x, y, cx, cy, s):
    """Transformasi Skala"""
    return cx + (x - cx)*s, cy + (y - cy)*s

def translate_point(x, y, tx, ty):
    """Transformasi Translasi"""
    return x + tx, y + ty

def refleksi_y(x, y):
    """Refleksi terhadap sumbu-Y"""
    return -x, y

# =========================
# POHON (Menggunakan POLIGON)
# =========================
def gambar_pohon(x, y):
    # Batang pohon
    tree_pen.color("saddlebrown")
    tree_pen.penup()
    tree_pen.goto(x - 10, y)
    tree_pen.pendown()
    tree_pen.begin_fill()
    tree_pen.goto(x + 10, y)
    tree_pen.goto(x + 10, y + 50)
    tree_pen.goto(x - 10, y + 50)
    tree_pen.goto(x - 10, y)
    tree_pen.end_fill()
    
    # Daun menggunakan ALGORITMA POLIGON FILL
    points1 = [(x - 40, y + 50), (x + 40, y + 50), (x, y + 90)]
    polygon_fill(points1, "forestgreen")
    
    points2 = [(x - 35, y + 70), (x + 35, y + 70), (x, y + 110)]
    polygon_fill(points2, "green")
    
    points3 = [(x - 30, y + 90), (x + 30, y + 90), (x, y + 130)]
    polygon_fill(points3, "limegreen")

# =========================
# KINCIR ANGIN (Menggunakan ROTASI)
# =========================
def gambar_kincir_angin(x, y, sudut):
    windmill_pen.clear()
    
    # Bangunan kincir (menara trapesium)
    windmill_pen.color("wheat")
    windmill_pen.penup()
    windmill_pen.goto(x - 35, y)
    windmill_pen.pendown()
    windmill_pen.begin_fill()
    windmill_pen.goto(x + 35, y)
    windmill_pen.goto(x + 25, y + 100)
    windmill_pen.goto(x - 25, y + 100)
    windmill_pen.goto(x - 35, y)
    windmill_pen.end_fill()
    
    # Detail garis horizontal
    windmill_pen.color("burlywood")
    for h in [20, 40, 60, 80]:
        w = 35 - (h * 0.1)
        windmill_pen.penup()
        windmill_pen.goto(x - w, y + h)
        windmill_pen.pendown()
        windmill_pen.goto(x + w, y + h)
    
    # Pintu
    windmill_pen.color("saddlebrown")
    windmill_pen.penup()
    windmill_pen.goto(x - 8, y)
    windmill_pen.pendown()
    windmill_pen.begin_fill()
    windmill_pen.goto(x + 8, y)
    windmill_pen.goto(x + 8, y + 25)
    windmill_pen.goto(x - 8, y + 25)
    windmill_pen.goto(x - 8, y)
    windmill_pen.end_fill()
    
    # Jendela (menggunakan MIDPOINT CIRCLE)
    windmill_pen.penup()
    windmill_pen.goto(x, y + 50)
    windmill_pen.pendown()
    for dy in range(-8, 9):
        if dy*dy <= 64:
            dx = int(math.sqrt(64 - dy*dy))
            windmill_pen.penup()
            windmill_pen.goto(x - dx, y + 50 + dy)
            windmill_pen.pendown()
            windmill_pen.color("lightblue")
            windmill_pen.goto(x + dx, y + 50 + dy)
    
    # Atap
    windmill_pen.color("darkred")
    windmill_pen.penup()
    windmill_pen.goto(x - 30, y + 100)
    windmill_pen.pendown()
    windmill_pen.begin_fill()
    windmill_pen.goto(x, y + 130)
    windmill_pen.goto(x + 30, y + 100)
    windmill_pen.goto(x - 30, y + 100)
    windmill_pen.end_fill()
    
    # Tiang baling-baling
    windmill_pen.color("gray")
    windmill_pen.width(3)
    windmill_pen.penup()
    windmill_pen.goto(x, y + 100)
    windmill_pen.pendown()
    windmill_pen.goto(x, y + 145)
    windmill_pen.width(1)
    
    # Pusat baling-baling
    windmill_pen.penup()
    windmill_pen.goto(x, y + 135)
    windmill_pen.pendown()
    windmill_pen.begin_fill()
    windmill_pen.color("darkgray")
    windmill_pen.circle(10)
    windmill_pen.end_fill()
    
    # Baling-baling dengan TRANSFORMASI ROTASI
    for i in range(4):
        angle = sudut + i * 90
        
        # Blade original
        blade_points = [
            (x + 8, y + 145),
            (x + 50, y + 140),
            (x + 50, y + 150)
        ]
        
        # ROTASI setiap titik
        rotated_points = []
        for px, py in blade_points:
            rx, ry = rotate_point(px, py, x, y + 145, angle)
            rotated_points.append((rx, ry))
        
        # Gambar blade
        windmill_pen.penup()
        windmill_pen.goto(rotated_points[0])
        windmill_pen.pendown()
        windmill_pen.begin_fill()
        windmill_pen.color("white")
        for point in rotated_points:
            windmill_pen.goto(point)
        windmill_pen.goto(rotated_points[0])
        windmill_pen.end_fill()

# =========================
# KUPU-KUPU (Menggunakan TRANSLASI + SKALA)
# =========================
def gambar_kupu(x, y, skala):
    butterfly_pen.clear()
    
    # Badan
    butterfly_pen.color("black")
    butterfly_pen.width(3)
    
    body_start = (0, -10)
    body_end = (0, 10)
    
    # SKALA + TRANSLASI
    bx1, by1 = scale_point(body_start[0], body_start[1], 0, 0, skala)
    bx1, by1 = translate_point(bx1, by1, x, y)
    
    bx2, by2 = scale_point(body_end[0], body_end[1], 0, 0, skala)
    bx2, by2 = translate_point(bx2, by2, x, y)
    
    butterfly_pen.penup()
    butterfly_pen.goto(bx1, by1)
    butterfly_pen.pendown()
    butterfly_pen.goto(bx2, by2)
    butterfly_pen.width(1)
    
    # Sayap (4 sayap dengan TRANSFORMASI)
    wings = [
        ([(-5, 0), (-15, 5), (-15, 12), (-8, 10)], "orange"),
        ([(-5, 0), (-12, -5), (-12, -10), (-6, -8)], "yellow"),
        ([(5, 0), (15, 5), (15, 12), (8, 10)], "orange"),
        ([(5, 0), (12, -5), (12, -10), (6, -8)], "yellow")
    ]
    
    for wing_points, color in wings:
        butterfly_pen.color(color)
        transformed = []
        for px, py in wing_points:
            # SKALA
            sx, sy = scale_point(px, py, 0, 0, skala)
            # TRANSLASI
            tx, ty = translate_point(sx, sy, x, y)
            transformed.append((tx, ty))
        
        butterfly_pen.penup()
        butterfly_pen.goto(transformed[0])
        butterfly_pen.pendown()
        butterfly_pen.begin_fill()
        for point in transformed:
            butterfly_pen.goto(point)
        butterfly_pen.goto(transformed[0])
        butterfly_pen.end_fill()

# =========================
# RUMAH (Menggunakan DDA LINE + MIDPOINT CIRCLE)
# =========================
def rumah(x, y):
    # Dinding
    pen.color("peachpuff")
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.begin_fill()
    pen.goto(x+200, y)
    pen.goto(x+200, y+120)
    pen.goto(x, y+120)
    pen.goto(x, y)
    pen.end_fill()

    # Atap
    pen.color("firebrick")
    pen.penup()
    pen.begin_fill()
    pen.goto(x-20, y+120)
    pen.goto(x+100, y+200)
    pen.goto(x+220, y+120)
    pen.goto(x-20, y+120)
    pen.end_fill()

    # Pintu
    pen.color("saddlebrown")
    pen.penup()
    pen.goto(x+90, y)
    pen.pendown()
    pen.begin_fill()
    pen.goto(x+120, y)
    pen.goto(x+120, y+70)
    pen.goto(x+90, y+70)
    pen.goto(x+90, y)
    pen.end_fill()

    # Jendela menggunakan MIDPOINT CIRCLE
    lingkaran_isi_midpoint(x+50, y+60, 15)
    lingkaran_isi_midpoint(x+150, y+60, 15)

# =========================
# TANAH & JALAN
# =========================
def tanah(warna="green"):
    pen.color(warna)
    pen.penup()
    pen.goto(-800, -200)
    pen.pendown()
    pen.begin_fill()
    pen.goto(800, -200)
    pen.goto(800, -350)
    pen.goto(-800, -350)
    pen.goto(-800, -200)
    pen.end_fill()

    # Jalan
    pen.color("black")
    pen.goto(-800, -300)
    pen.begin_fill()
    pen.goto(800, -300)
    pen.goto(800, -250)
    pen.goto(-800, -250)
    pen.goto(-800, -300)
    pen.end_fill()

    # Marka jalan menggunakan DDA LINE
    pen.color("white")
    x = -780
    while x < 800:
        dda_line(x, -275, x+40, -275, "white")
        x += 80

    rumah(-100, -200)

# =========================
# MOBIL (Menggunakan TRANSLASI)
# =========================
mobil_x = -650
arah = 1
LANE_ATAS = -255
LANE_BAWAH = -285

def gambar_mobil(x_pos, arah, y_lane):
    car_pen.clear()
    car_pen.color("blue")

    # Titik-titik mobil dalam koordinat lokal
    body = [
        (0, 0), (100, 0), (100, 30),
        (70, 30), (50, 50),
        (20, 50), (0, 30)
    ]

    hasil = []

    for px, py in body:
        # REFLEKSI Sumbu-Y jika arah ke kiri
        if arah == -1:
            px, py = refleksi_y(px, py)

        # TRANSLASI ke posisi mobil
        tx, ty = translate_point(px, py, x_pos, y_lane)
        hasil.append((tx, ty))

    # Gambar badan mobil
    car_pen.penup()
    car_pen.goto(hasil[0])
    car_pen.pendown()
    car_pen.begin_fill()
    for p in hasil:
        car_pen.goto(p)
    car_pen.goto(hasil[0])
    car_pen.end_fill()

    # Jendela (ikut refleksi)
    car_pen.color("lightblue")
    jendela = [(30, 30), (55, 30), (40, 45), (25, 45), (10, 29)]
    hasil_jendela = []

    for px, py in jendela:
        if arah == -1:
            px, py = refleksi_y(px, py)
        tx, ty = translate_point(px, py, x_pos, y_lane)
        hasil_jendela.append((tx, ty))

    car_pen.penup()
    car_pen.goto(hasil_jendela[0])
    car_pen.pendown()
    car_pen.begin_fill()
    for p in hasil_jendela:
        car_pen.goto(p)
    car_pen.goto(hasil_jendela[0])
    car_pen.end_fill()

    # Roda (ikut refleksi)
    roda = [(25, -5), (75, -5)]
    for px, py in roda:
        if arah == -1:
            px, py = refleksi_y(px, py)
        tx, ty = translate_point(px, py, x_pos, y_lane)
        car_pen.penup()
        car_pen.goto(tx, ty)
        car_pen.dot(14, "grey")


# =========================
# ASSET LANGIT
# =========================
screen.addshape("assets/matahari.gif")
screen.addshape("assets/bulan.gif")
screen.addshape("assets/awan.gif")
screen.addshape("assets/awan_kecil.gif")

sun = turtle.Turtle()
sun.hideturtle()
sun.penup()
sun.shape("assets/matahari.gif")

moon = turtle.Turtle()
moon.hideturtle()
moon.penup()
moon.shape("assets/bulan.gif")

clouds = []
for pos, shp in [((-500,230),"assets/awan.gif"),
                 ((-200,260),"assets/awan.gif"),
                 ((-100,200),"assets/awan_kecil.gif")]:
    c = turtle.Turtle()
    c.hideturtle()
    c.penup()
    c.shape(shp)
    c.goto(pos)
    c.showturtle()
    clouds.append(c)

# =========================
# BINTANG
# =========================
stars = [(random.randint(-600,600), random.randint(50,250)) for _ in range(80)]
star_pen = turtle.Turtle()
star_pen.hideturtle()
star_pen.penup()

# =========================
# VARIABEL ANIMASI
# =========================
angle = 0
fase = "siang"
kincir_sudut = 0
kupu_x = 300
kupu_y = 100
kupu_arah = 1
kupu_skala = 1.0
kupu_skala_arah = 0.02

# =========================
# ANIMASI UTAMA
# =========================
def animasi():
    global mobil_x, arah, angle, fase, kincir_sudut
    global kupu_x, kupu_y, kupu_arah, kupu_skala, kupu_skala_arah

    pen.clear()
    star_pen.clear()
    tree_pen.clear()

    tanah("darkgreen" if fase=="malam" else "green")

    # Animasi matahari/bulan
    angle += 2
    x = -600 + (1200 * angle / 180)
    y = -150 + (250 * math.sin(math.radians(angle)))

    if fase == "siang":
        sun.goto(x, y)
        sun.showturtle()
        moon.hideturtle()
        if angle >= 180:
            angle = 0
            fase = "malam"
            screen.bgcolor("midnightblue")
    else:
        moon.goto(x, y)
        moon.showturtle()
        sun.hideturtle()
        for sx, sy in stars:
            star_pen.goto(sx, sy)
            star_pen.dot(2, "white")
        if angle >= 180:
            angle = 0
            fase = "siang"
            screen.bgcolor("skyblue")

    # Animasi awan (TRANSLASI)
    for c in clouds:
        cx, cy = c.position()
        c.goto(cx+1.2, cy)
        if cx > 650:
            c.goto(-650, cy)

    # Kincir angin (DIGAMBAR PERTAMA - di belakang)
    kincir_sudut += 5
    gambar_kincir_angin(-450, -200, kincir_sudut)
    
    # Pohon (DI DEPAN kincir)
    gambar_pohon(-400, -200)
    gambar_pohon(350, -200)

    # Mobil (TRANSLASI)
    if arah == 1:
        y_mobil = LANE_ATAS
    else:
        y_mobil = LANE_BAWAH

    gambar_mobil(mobil_x, arah, y_mobil)
    mobil_x += 5 * arah
    if mobil_x > 700:
        arah = -1 #kiri
    if mobil_x < -700:
        arah = 1 #kanan
    
    # Kupu-kupu (TRANSLASI + SKALA)
    kupu_x += 2 * kupu_arah
    if kupu_x > 450:
        kupu_arah = -1
    if kupu_x < 250:
        kupu_arah = 1
    
    kupu_skala += kupu_skala_arah
    if kupu_skala > 1.3:
        kupu_skala_arah = -0.02
    if kupu_skala < 0.8:
        kupu_skala_arah = 0.02
    
    gambar_kupu(kupu_x, kupu_y, kupu_skala)

    screen.update()
    screen.ontimer(animasi, 60)

# =========================
# JALANKAN PROGRAM
# =========================
animasi()
turtle.done()
