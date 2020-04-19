from tkinter import *
from math import *

x_os = 400
y_os = 300
X = 400
Y = 300


def line(star,canvas,P1,P2,w=2,color="red"):
    canvas.create_line(star[P1][0],star[P1][1],star[P2][0],star[P2][1],width=w,fill=color)

def point(canvas,x1,y1,w=1,color='red'):
    canvas.create_oval(x1, y1, x1, y1, width=w, outline=color)

def pentagon(canvas,dict,Radius,color='red'):
    line(dict,canvas, "A", "a"),line(dict,canvas, "a", "B"),line(dict,canvas, "B", "b"),line(dict,canvas, "b", "C"),line(dict,canvas, "C", "c"),line(dict,canvas, "c", "D"),line(dict,canvas, "D", "d"),line(dict,canvas, "d", "E"),line(dict,canvas, "E", "e"),line(dict,canvas, "e", "A")
    #canvas.create_polygon(dict['A'],dict['a'],dict['B'],dict['b'],dict['C'],dict['c'],dict['D'],dict['d'],dict['E'],dict['e'],fill=color)
    Radius *= 0.9
    '''canvas.create_arc(X - Radius,Y - Radius, X + Radius, Y + Radius, start=-15, extent=65)
    canvas.create_arc(X - Radius,Y - Radius, X + Radius, Y + Radius, start=50, extent=80)
    canvas.create_arc(X - Radius,Y - Radius, X + Radius, Y + Radius, start=130, extent=65)
    canvas.create_arc(X - Radius,Y - Radius, X + Radius, Y + Radius, start=195, extent=75)
    canvas.create_arc(X - Radius,Y - Radius, X + Radius, Y + Radius, start=270, extent=75)'''
    #line(dict,canvas, "A", "B",1,'black'),line(dict,canvas, "B", "C",1,'black'),line(dict,canvas, "C", "D",1,'black'),line(dict,canvas, "D", "E",1,'black'),line(dict,canvas, "E", "A",1,'black')
    '''canvas.create_line(dict['A'][0], dict['A'][1], dict['C'][0], dict['C'][1], width=1, fill="black")
    canvas.create_line(dict['B'][0], dict['B'][1], dict['D'][0], dict['D'][1], width=1, fill="black")
    canvas.create_line(dict['B'][0], dict['B'][1], dict['D'][0], dict['D'][1], width=1, fill="black")
    canvas.create_line(dict['E'][0], dict['E'][1], dict['C'][0], dict['C'][1], width=1, fill="black")
    canvas.create_line(dict['E'][0], dict['E'][1], dict['B'][0], dict['B'][1], width=1, fill="black")
    canvas.create_line(dict['A'][0], dict['A'][1], dict['D'][0], dict['D'][1], width=1, fill="black")'''

def circle(canvas,R,xx = X,yy = Y):
    circle_ = lambda r, x: sqrt(r ** 2 - x ** 2)

    for i in range(10000):
        try:
            x = xx - i * (1/10)
            point(canvas, x + xx, circle_(R, x) + yy)
            point(canvas, x + xx, yy - circle_(R, x))
        except: pass

def draw():
    root = Tk()

    canvas = Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    Radius = int(e1.get())
    small_circle = int(e2.get())
    Star_radius = Radius * 0.8

    star = {'A': ([X], [Y - Star_radius]),
            'B': ([X + Star_radius - Star_radius / 18], [Y - Star_radius / 3 * 0.83]),
            'C': ([X + Star_radius * 0.6], [Y + Star_radius - Star_radius / 5]),
            'D': ([X - Star_radius * 0.6], [Y + Star_radius - Star_radius / 5]),
            'E': ([X - Star_radius + Star_radius / 18], [Y - Star_radius / 3 * 0.83]),
            'a': ([X + Star_radius / 3 - Star_radius/14], [Y - Star_radius / 3 + Star_radius/23]),
            'b': ([X + Star_radius / 2.7], [Y + Star_radius/10]),
            'c': ([X], [Y + Star_radius/2.6]),
            'd': ([X - Star_radius / 2.7], [Y + Star_radius/10]),
            'e': ([X - Star_radius / 3 + Star_radius/14], [Y - Star_radius / 3 + Star_radius/23])
            }

    for y in range(1,100):
        k = y * 10
        canvas.create_line(k, 0, k, 600, width=1, fill='#deddfa')
    for x in range(1,60):
        k = x * 10
        canvas.create_line(0, k, 1000, k, width=1, fill='#deddfa')

    canvas.create_line(x_os, 800, x_os, 0, width=2, arrow=LAST)
    canvas.create_text(x_os + 15, 15, text='y', fill="black", font=("Helvectica", "10"))
    canvas.create_line(0, y_os, 800, y_os, width=2, arrow=LAST)
    canvas.create_text(x_os * 2 - 15, y_os - 15, text='x', fill="black", font=("Helvectica", "10"))
    canvas.create_line(x_os - 3, y_os - 25, x_os + 3, y_os - 25, width=1)
    canvas.create_text(x_os + 11, y_os - 25, text='25', fill="black", font=("Helvectica", "10"))
    canvas.create_line(x_os + 25, y_os - 3, x_os + 25, y_os + 3, width=1)
    canvas.create_text(x_os + 25, y_os - 11, text='25', fill="black", font=("Helvectica", "10"))

    pentagon(canvas, star, Radius)

    radius = Radius * 0.8
    circle(canvas,Radius/1.1)                                          #Biggest
    circle(canvas, small_circle, X + radius * 0.51, Y - radius * 0.61)    #1
    circle(canvas, small_circle, X + radius * 0.79, Y + radius * 0.21)    #2
    circle(canvas, small_circle, X, Y + radius*0.8)                       #3
    circle(canvas, small_circle, X - radius * 0.79, Y + radius * 0.21)    #4
    circle(canvas, small_circle, X - radius * 0.51, Y - radius * 0.61)    #5

    root.mainloop()

master = Tk()
Label(master,text="Greatest Radius").grid(row=0)
Label(master,text="Smaller Radius").grid(row=1)

RRR = 250
AltRadius = IntVar()
AltRadius.set(RRR)
e1 = Entry(master, textvariable=AltRadius)
AltSmallRadius = IntVar()
AltSmallRadius.set(int(RRR/8))
e2 = Entry(master, textvariable=AltSmallRadius)

e1.grid(row=0, column=1,pady=2)
e2.grid(row=1, column=1,pady=2)

Button(master,text='Show', command=draw, width=17).grid(row=3,column=1,sticky=W,pady=2)

if __name__ == "__main__":
    mainloop()
