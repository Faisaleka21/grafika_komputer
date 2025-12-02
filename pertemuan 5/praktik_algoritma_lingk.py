# praktik
import turtle

def midpoint_circle(r):
    x=0
    y=r
    p=1-r
    points=[]
    
    while x<=y:
        # 8 titik untuk buat lingkaran
        points.extend([
            (x, y),
            (y, x),
            (-x, y),
            (-y, x),
            (x, -y),
            (y, -x),
            (-x, -y),
            (-y, -x)
            ])
        x+=1  #jika nilainya makin besar jarak titik mekin lebar
        
        if p<0:
            p = p+2*x+3
        elif p>=0:
            y=y-1
            p=p+2*(x-y)+5
            
    return points
     

# fungsi untuk menggambar ttik di turtle
def draw_points(points, scale=20): #scale ini jarak antar titik. scale=2 agar hasilnya garis
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    
    #gambar sumbu bantu(opsional)
    turtle.goto(0,0)
    turtle.dot(1, 'red') #titik merah di pusat dengan radius/ukurannya 6 px
    
    for x,y in points:
        turtle.goto(x*scale, y*scale)
        turtle.dot(5, 'black') #titik hitam unutk membuat titik bentuk lingkaran size 6px/ tingkat ketebalan
        
    turtle.done()
        
# jalankan program (radius 6)

r=20 
points = midpoint_circle(r)
draw_points(points)