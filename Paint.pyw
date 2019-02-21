from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
from PIL import ImageGrab

canvas_width = 700
canvas_height = 500

size = 1
color = '#000000'
rgb = (0, 0, 0)

lst = ['Черный', 'Красный', 'Зеленый', 'Голубой', 'Желтый', 'Белый',
       'Выбор цвета',
       color,
       'white', 'yellow', 'blue', 'green', 'red', 'black']

root = Tk()
root.title("Paint Python")
root.geometry('+1+1')


def activate_paint(e):
    global x1, y1, size, color
    x1, y1 = e.x, e.y

    if size != scl.get():
        for obj in list_btnSize:
            obj.configure(relief=RAISED, state=NORMAL)

    color = lstBox.get(lstBox.curselection())
    size = scl.get()
    txt()

    if var.get() == 0:
        w.bind('<B1-Motion>', paint_oval)
    elif var.get() == 2:
        w.bind('<B1-Motion>', paint_line)
    else:
        w.bind('<B1-Motion>', paint_line, add="+")
        w.bind('<B1-Motion>', paint_oval, add="+")


def txt():
    global rgb, color
    if color == 'black':
        color = '#000000'
        rgb = (0, 0, 0)
    elif color == 'white':
        color = '#ffffff'
        rgb = (255, 255, 255)
    elif color == 'red':
        color = '#ff0000'
        rgb = (255, 0, 0)
    elif color == 'green':
        color = '#008000'
        rgb = (0, 128, 0)
    elif color == 'blue':
        color = '#0000ff'
        rgb = (0, 0, 255)
    elif color == 'yellow':
        color = '#ffff00'
        rgb = (255, 255, 0)

    text_rgb.delete(1.0, END)
    text_rgb.insert(1.0, f' {color} \n {int(rgb[0]), int(rgb[1]), int(rgb[2])}')


def paint_line(e):
    global x1, y1
    x2, y2 = e.x, e.y
    w.create_line((x1, y1, x2, y2), width=size, fill=color)
    x1, y1 = x2, y2


def paint_oval(e):
    x, y = e.x, e.y
    r = size // 2
    w.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='')


def size_change(new_size, pressBtn):
    global size
    size = new_size
    scl.set(size)

    for obj in list_btnSize:
        obj.configure(relief=SUNKEN if list_btnSize[pressBtn] is obj else RAISED,
                      state=DISABLED if list_btnSize[pressBtn] is obj else NORMAL)


def color_change(new_color):
    global index
    # переустанавливаем цвет в Listbox
    lstBox.delete(0, END)
    for element in lst[-1:6:-1]:
        lstBox.insert(END, element)
    if new_color in lst:
        index = (len(lst) - 1) - lst.index(new_color)
    lstBox.selection_set(first=index)
    lstBox.activate(index)


def color_all():
    global rgb, color
    color_old = color
    rgb_old = rgb
    rgb, new_col = colorchooser.askcolor()
    if new_col is None:  # нажата кнопка "Отмена"
        rgb = rgb_old
        new_col = color_old
    lst[len(lst)//2] = new_col
    return color_change(new_col)


def clear():
    w.delete("all")
    text_rgb.delete(1.0, END)


def new_file():
    clear()


def open_file():
    global fn
    try:
        file_name = fd.askopenfilename()
        fn = PhotoImage(file=file_name)
        w.create_image(w.winfo_width()/2, w.winfo_height()/2, image=fn)
    except (FileNotFoundError, ValueError, TclError):
        pass


def save_file():
    try:
        file_name = fd.asksaveasfilename(defaultextension='.png',
                                         filetypes=(('PNG files', '*.png'),
                                                    ('All files', '*.*')))
        x_1 = w.winfo_rootx() + w.winfo_x()
        y_1 = w.winfo_rooty() + w.winfo_y()
        x_2 = x_1 + w.winfo_width() * 1.25
        y_2 = y_1 + w.winfo_height() * 1.15
        xy = (x_1, y_1, x_2, y_2)
        ImageGrab.grab(xy).save(file_name)
        # print(file_name)
    except (FileNotFoundError, ValueError):
        pass


filemenu = Menu(root)
root.config(menu=filemenu)
submenu = Menu(filemenu, tearoff=0)
submenu.add_command(label="Новый", command=new_file)
submenu.add_command(label="Открыть", command=open_file)
submenu.add_command(label="Сохранить", command=save_file)
filemenu.add_cascade(label="Файл", menu=submenu)

w = Canvas(root, width=canvas_width, height=canvas_height,
           bg="white", cursor='spider')
w.bind('<Button-1>', activate_paint)  # <1>
w.grid(row=2, column=0, columnspan=6, padx=3, pady=3, sticky=E + W + S + N)

list_btnSize = []
for i in range(len(lst)//2):
    def com(new_col=lst[-1-i]): return color_change(new_col)
    Button(text=lst[i], width=16, fg=lst[-1-i], bg='light grey',
           font='arial 9',
           command=com if i < len(lst)/2-1 else color_all).grid(row=0,
                                                                column=i)

    def comm(neu_sz=1+i*2, press=i): return size_change(neu_sz, press)
    btn = Button(text=1+i*2 if i < len(lst)/2-1 else 'Очистить',
                 width=16, bg='light grey', fg='navy', font='arial 9',
                 command=comm if i < len(lst)/2-1 else clear)
    btn.configure(relief=RAISED, state=NORMAL)
    btn.grid(row=1, column=i)
    list_btnSize.append(btn)

lfList = LabelFrame(root, text=' Список ', bd=2, relief=SUNKEN, fg='navy')
lfList.grid(row=2, column=6, sticky=N + W + E)
lstBox = Listbox(lfList, selectmode=BROWSE,
                 bd=3, width=16, height=7)  # selectmode=SINGLE
for elem in lst[-1:6:-1]:
    lstBox.insert(END, elem)
lstBox.selection_set(first=0)
lstBox.pack()

lfText = LabelFrame(root, text=' HEX, RGB ', fg='navy', width=122, height=62)
lfText.pack_propagate(False)
lfText.place(x=730, y=190)
text_rgb = Text(lfText, font='arial 12 bold', fg='gray25', bg='light gray')
text_rgb.pack()

scl = Scale(root, orient=VERTICAL, length=234, from_=0, to=100,
            tickinterval=10, resolution=1, relief=SUNKEN)
scl.set(size)
scl.place(x=730, y=252)

var = IntVar()
var.set(1)
tx = ['oval', 'mix', 'line']
for i in range(len(tx)):
    Radiobutton(root, text=tx[i], variable=var, fg='navy',
                value=i).place(x=740+i*25, y=520 if i == 1 else 500)

root.mainloop()
