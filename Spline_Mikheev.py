#UI.py

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, Tk, Frame, Label, Entry, Button, Scrollbar, RIGHT, Y, NO, CENTER
from spline import *


#UI
ws = Tk()

ws.title('Таблица значений (x,y)')
ws.geometry('300x350')

Input_frame = Frame(ws)
Input_frame.pack()

x_l = Label(Input_frame,text="X")
x_l.grid(row=0,column=0)

y_l = Label(Input_frame,text="Y")
y_l.grid(row=0,column=1)

x_entries = []
y_entries = []

for i in range(1, 13):
    x_entry = Entry(Input_frame)
    x_entry.grid(row=i,column=0)
    x_entries.append(x_entry)

    y_entry = Entry(Input_frame)
    y_entry.grid(row=i,column=1)
    y_entries.append(y_entry)
    
def input_record():
    global a_x
    var.a_x = [x_entry.get() for x_entry in x_entries]
    var.a_x = arr_resize(var.a_x)
    var.a_x = array(var.a_x, dtype=float32)
    
    global a_y
    var.a_y = [y_entry.get() for y_entry in y_entries]
    var.a_y = arr_resize(var.a_y)
    var.a_y = array(var.a_y, dtype=float32)
    

    
def figure():
#graph
    var.a_x, var.a_y = insertion_sort(var.a_x, var.a_y)
    var.a, var.b, var.c, var.d = build_spline(var.a_x, var.a_y)
    
    x_vals = linspace(min(var.a_x), max(var.a_x), 1000)
    y_vals = []
    
    for i in x_vals:
        y_vals.append(interpolate(var.a, var.b, var.c, var.d, var.a_x, i))
    
    root = Tk()
    root.title ("Graph")
    root.geometry("700x1000")

    # for i, x in enumerate(var.a_x):
    #    assert abs(var.a_y[i] - spline(x)) < 1e-8, f'Error at {x}, {a_y[i]}'
    
    fig = Figure(figsize=(8,8), dpi=100)
    figa = fig.add_subplot(111)
    
    figa.plot(x_vals, y_vals)
    figa.scatter(var.a_x, var.a_y, color='red', s=10, marker='o')
    figa.grid()
    
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()
    canvas.get_tk_widget().pack()

#tab
    tab_frame = Frame(root)
    tab_frame.pack()
    
    #scrollbar
    tab_scroll = Scrollbar(tab_frame)
    tab_scroll.pack(side=RIGHT, fill=Y)
    tab = ttk.Treeview(tab_frame, yscrollcommand=tab_scroll.set)
    tab.pack()
    tab_scroll.config(command=tab.yview)

    #frames
    tab['columns'] = ('intervals','A_value', 'B_value', 'C_value', 'D_value')

    tab.column("#0", width=0,  stretch=NO)
    tab.column("intervals",anchor=CENTER,width=80)
    tab.column("A_value",anchor=CENTER,width=80)
    tab.column("B_value",anchor=CENTER,width=100)
    tab.column("C_value",anchor=CENTER,width=100)
    tab.column("D_value",anchor=CENTER,width=100)

    tab.heading("#0",text="",anchor=CENTER)
    tab.heading("intervals",text="intervals",anchor=CENTER)
    tab.heading("A_value",text="A",anchor=CENTER)
    tab.heading("B_value",text="B",anchor=CENTER)
    tab.heading("C_value",text="C",anchor=CENTER)
    tab.heading("D_value",text="D",anchor=CENTER)

    for i in range (1, len(var.a)):
        tab.insert(parent='',index='end',iid=i,text='',values=(str(var.a_x[i-1])+' - '+str(var.a_x[i]),var.a[i],var.b[i],var.c[i],var.d[i]))

    tab.pack()
    root.mainloop()
    
#buttons
Input_button = Button(ws,text = "Сохранить значения",command= input_record)
Input_button.pack()
Graph_button = Button(ws,text = "Построить сплайн", command = figure)
Graph_button.pack()

ws.mainloop()