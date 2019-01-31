from tkinter import *

canvas_width = 700
canvas_height = 500
size = 1
color = "black"
lx, ly = None, None


def activate_paint(e):
    global lx, ly
    lx, ly = e.x, e.y

    if var.get() == 0:
        w.bind('<B1-Motion>', paint_oval)
    elif var.get() == 2:
        w.bind('<B1-Motion>', paint_line)
    else:
        w.bind('<B1-Motion>', paint_line, add="+")
        w.bind('<B1-Motion>', paint_oval, add="+")


def paint_line(e):
    global lx, ly
    color = lstBox.get(lstBox.curselection())
    size = scl.get()
    x, y = e.x, e.y
    w.create_line((lx, ly, x, y), width=size, fill=color)
    lx, ly = x, y


def paint_oval(e):
    color = lstBox.get(lstBox.curselection())
    size = scl.get() / 2
    x1 = e.x - size
    x2 = e.x + size
    y1 = e.y - size
    y2 = e.y + size
    w.create_oval(x1, y1, x2, y2, fill=color, outline=color)


def size_change(new_size):
    global size
    size = new_size
    scl.set(size)


def color_change(new_color):
    global color
    color = new_color
    # переустанавливаем выбранное значение в Listbox
    lstBox.delete(0, END)
    for elem in list_btn[-1:5:-1]:
        lstBox.insert(END, elem)
    index = (len(list_btn) - 1) - list_btn.index(color)
    lstBox.selection_set(first=index)
    lstBox.activate(index)


root = Tk()
root.title("Рисовалка на Python")

w = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
w.bind('<1>', activate_paint)
w.grid(row=2, column=0, columnspan=6, padx=3, pady=3, sticky=E + W + S + N)
# w.columnconfigure(6, weight=10)
# w.rowconfigure(2, weight=1)

list_btn = ["Черный", "Красный", "Зеленый", "Голубой", "Желтый", "Белый",
            'white', 'yellow', 'blue', 'green', 'red', 'black']

for i in range(len(list_btn)//2):
    def com(col=list_btn[-1-i]): return color_change(col)
    Button(text=list_btn[i], width=16, fg=list_btn[-1-i], bg='light grey', font='arial 9',
           command=com).grid(row=0, column=i)

    def comm(s=1+i*2): return size_change(s)
    Button(text=1+i*2, width=16, bg='light grey', command=comm).grid(row=1, column=i)

Button(root, text="Очистить", width=14, bd=3,
       font='arial 9 bold', fg='white', bg='black',
       command=lambda: w.delete("all")).grid(row=0, column=6, sticky=W)

lfList = LabelFrame(root, text=' Список ', bd=2, relief=SUNKEN, fg='blue')
lfList.grid(row=1, column=6, sticky=N + W + E, rowspan=2)
lstBox = Listbox(lfList, selectmode=BROWSE, bd=3, width=16, height=6)  # selectmode=SINGLE
for elem in list_btn[-1:5:-1]:
    lstBox.insert(END, elem)
lstBox.selection_set(first=0)
lstBox.pack()

scl = Scale(root, orient=VERTICAL, length=234, from_=0, to=100,
            tickinterval=10, resolution=1, relief=SUNKEN)
scl.set(size)
scl.grid(row=2, column=6)

var = IntVar()
var.set(1)
tx = ['oval', 'mix', 'line']
for i in range(len(tx)):
    Radiobutton(root, text=tx[i],
                variable=var, value=i).place(x=740+i*25, y=500 if i == 1 else 480)

root.mainloop()
