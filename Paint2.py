from tkinter import *
import time
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog as fd
# from tkinter import messagebox as mb
from PIL import Image, ImageDraw, ImageTk
try:
    from PIL import ImageGrab
except BaseException:
    import pyscreenshot as ImageGrab  # For Linux

color = '#000000'
rgb = (0, 0, 0)
t = 'Черный:'
WIDTH = 640
HEIGHT = 480

# создаем окно
root = Tk()
root.geometry('800x620+0+0')
'''
if sys.platform.startswith('win'):
    root.iconbitmap('img/label.ico')
else:
    root.call('wm', 'iconphoto', root._w, PhotoImage(file='img/label.png'))
'''
root.iconphoto(True, PhotoImage(file='img/label.png'))
root.title('Paint')

# создаем холст в окне
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white', cursor='spider')
canvas.place(x=130, y=90)

can = Canvas(root, width=95, height=55, bg='white', relief=SUNKEN, bd=10)
can.place(x=5, y=5)

# рисуем изображение в PIL
imag = Image.new('RGBA', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(imag)


def activate_paint(event):
    global x, y, size
    x, y = event.x, event.y

    if var.get() == 0:
        sc.set(10)
    elif var.get() == 1:
        sc.set(20)
    elif var.get() == 2:
        sc.set(30)
    elif var.get() == 3:
        sc.set(40)
    elif var.get() == 4:
        sc.set(50)
    size = sc.get()

    if var2.get() == 1:
        canvas.bind('<B1-Motion>', paint_oval)
    elif var2.get() == 2:
        canvas.bind('<B1-Motion>', paint_line)
    else:
        if size > 1:
            canvas.bind('<B1-Motion>', paint_line, add="+")
            canvas.bind('<B1-Motion>', paint_oval, add="+")
        else:
            canvas.bind('<B1-Motion>', paint_line)

    text_pos.delete(1.0, END)
    text_pos2.delete(1.0, END)
    text_pos.insert(1.0, f' x: {x} \n y: {y} ')
    # text_pos.insert(1.0, ' x: {}\n y: {}'.format(x, y))
    text_pos2.insert(1.0,
                     f' {t} \n {color} \n {int(rgb[0]), int(rgb[1]), int(rgb[2])}')


def paint_line(event):
    global x, y
    x2, y2 = event.x, event.y
    canvas.create_line((x, y, x2, y2), width=size, fill=color)
    draw.line((x, y, x2, y2), width=size, fill=color)
    x, y = x2, y2


def paint_oval(event):
    x, y = event.x, event.y
    r = size // 2
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='')
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=color)


def clean(event):
    new_file()


def tick():
    lb1['text'] = time.strftime('%H:%M:%S')
    lb1.after(200, tick)


def color_all(event):
    global color, rgb, t
    color_old = color
    rgb_old = rgb
    rgb, color = colorchooser.askcolor()
    if color is None:
        color = color_old
        rgb = rgb_old
    t = 'Выбран цвет:'
    btn_3.configure(relief=RAISED, state=NORMAL)
    btn_4.configure(relief=RAISED, state=NORMAL)
    btn_5.configure(relief=RAISED, state=NORMAL)
    btn_6.configure(relief=RAISED, state=NORMAL)
    btn_7.configure(relief=RAISED, state=NORMAL)


def color_red(event):
    global color, rgb, t
    rgb = (255, 0, 0)
    color = '#ff0000'
    t = 'Красный:'
    btn_3.configure(relief=SUNKEN, state=DISABLED, disabledforeground='white')
    btn_2.configure(relief=RAISED, state=NORMAL)
    btn_4.configure(relief=RAISED, state=NORMAL)
    btn_5.configure(relief=RAISED, state=NORMAL)
    btn_6.configure(relief=RAISED, state=NORMAL)
    btn_7.configure(relief=RAISED, state=NORMAL)


def color_green(event):
    global color, rgb, t
    rgb = (0, 255, 0)
    color = '#00ff00'
    t = 'Зеленый:'
    btn_4.configure(relief=SUNKEN, state=DISABLED, disabledforeground='white')
    btn_2.configure(relief=RAISED, state=NORMAL)
    btn_3.configure(relief=RAISED, state=NORMAL)
    btn_5.configure(relief=RAISED, state=NORMAL)
    btn_6.configure(relief=RAISED, state=NORMAL)
    btn_7.configure(relief=RAISED, state=NORMAL)


def color_blue(event):
    global color, rgb, t
    rgb = (0, 0, 255)
    color = '#0000ff'
    t = 'Синий:'
    btn_5.configure(relief=SUNKEN, state=DISABLED, disabledforeground='white')
    btn_2.configure(relief=RAISED, state=NORMAL)
    btn_3.configure(relief=RAISED, state=NORMAL)
    btn_4.configure(relief=RAISED, state=NORMAL)
    btn_6.configure(relief=RAISED, state=NORMAL)
    btn_7.configure(relief=RAISED, state=NORMAL)


def color_black(event):
    global color, rgb, t
    rgb = (0, 0, 0)
    color = '#000000'
    t = 'Черный:'
    btn_6.configure(relief=SUNKEN, state=DISABLED, disabledforeground='white')
    btn_2.configure(relief=RAISED, state=NORMAL)
    btn_3.configure(relief=RAISED, state=NORMAL)
    btn_4.configure(relief=RAISED, state=NORMAL)
    btn_5.configure(relief=RAISED, state=NORMAL)
    btn_7.configure(relief=RAISED, state=NORMAL)


def lastik(event):
    global color, rgb, t
    rgb = (255, 255, 255)
    color = '#ffffff'
    t = 'Ластик:'
    btn_7.configure(relief=SUNKEN, state=DISABLED, disabledforeground='black')
    btn_2.configure(relief=RAISED, state=NORMAL)
    btn_3.configure(relief=RAISED, state=NORMAL)
    btn_4.configure(relief=RAISED, state=NORMAL)
    btn_5.configure(relief=RAISED, state=NORMAL)
    btn_6.configure(relief=RAISED, state=NORMAL)


def new_file():
    global imag, draw

    canvas.delete(ALL)
    text_pos.delete(1.0, END)
    text_pos2.delete(1.0, END)

    imag.close()
    imag = Image.new('RGBA', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(imag)


def open_file():
    global imag, imag_tk
    try:
        file_name = fd.askopenfilename()
        imag = Image.open(file_name)
        imag_tk = ImageTk.PhotoImage(image=imag)
        canvas.create_image(0, 0, anchor=NW, image=imag_tk)
    except (FileNotFoundError, ValueError, TclError):
        pass


def save_file():
    try:
        file_name = fd.asksaveasfilename(defaultextension='.png',
                                         filetypes=(('PNG files', '*.png'),
                                                    ('All files', '*.*')))
        x_1 = canvas.winfo_rootx() + canvas.winfo_x()
        y_1 = canvas.winfo_rooty() + canvas.winfo_y()
        x_2 = x_1 + WIDTH
        y_2 = y_1 + HEIGHT
        xy = (x_1, y_1, x_2, y_2)
        ImageGrab.grab(xy).save(file_name)

        print(WIDTH, canvas.winfo_width())
    except (FileNotFoundError, ValueError):
        pass


def save_file2():
    try:
        file_name = fd.asksaveasfilename(defaultextension='.png',
                                         filetypes=(('PNG files', '*.png'),
                                                    ('All files', '*.*')))
        imag.save(file_name)
    except (FileNotFoundError, ValueError):
        pass


def activate_fill(event):
    global fill_activate
    fill_activate = True
    btn_8.configure(relief=SUNKEN, state=DISABLED)
    canvas.bind('<Button-1>', fill_, add='+')


def fill_(event):
    global tk_imag, fill_activate
    xf, yf = event.x, event.y
    if fill_activate is True:
        # заливка изображение
        rgba = int(rgb[0]), int(rgb[1]), int(rgb[2]), 255
        ImageDraw.floodfill(imag, xy=(xf, yf), value=rgba)
        # рисуем на холсте
        tk_imag = ImageTk.PhotoImage(image=imag)
        canvas.create_image(0, 0, anchor=NW, image=tk_imag)
        # деактивация кнопки и заливки
        btn_8.configure(relief=RAISED, state=NORMAL)
        fill_activate = False


def about():
    top = Toplevel()
    top.geometry('+120+120')
    top.title('About')
    top.minsize(width=200, height=100)
    label_about = Label(top, fg='red',
                        text='Это мое самое лучшее \nприложение для рисования')
    label_about.pack()


def mouse_right(event):
    menu_right.post(event.x_root, event.y_root)


def text():
    canvas.create_text(WIDTH / 2.0, HEIGHT / 2.0, justify=CENTER, text='PAINT',
                       font='times 50 bold', fill=color)


def set_size(d):
    d = sc.get() // 4
    w = can.winfo_width() / 2.0
    h = can.winfo_height() / 2.0
    can.delete('id')
    can.create_oval(w - d, h - d, w + d, h + d,
                    fill='white', outline=color, tag='id', width=5)


filemenu = Menu(root)
root.config(menu=filemenu)
submenu = Menu(filemenu, tearoff=0)
submenu.add_command(label="Новый", command=new_file)
submenu.add_command(label="Открыть", command=open_file)
submenu.add_command(label="Сохранить 1", command=save_file)
submenu.add_command(label="Сохранить 2", command=save_file2)
submenu.add_separator()
submenu.add_command(label="Выход", command=root.destroy)
filemenu.add_cascade(label="Файл", menu=submenu)

helpmenu = Menu(filemenu, tearoff=0)
helpmenu.add_command(label='О программе', command=about)
filemenu.add_cascade(label='Помощь', menu=helpmenu)

menu_right = Menu(tearoff=0)
menu_right.add_command(label='Text', command=text)
canvas.bind('<Button-3>', mouse_right)

lf1 = LabelFrame(root, text=' Координаты ', width=130, height=90, relief=SUNKEN)
lf1.pack_propagate(False)
lf1.place(x=0, y=90)
lf2 = LabelFrame(root, text=' Цвета ', width=130, height=90, relief=SUNKEN)
lf2.pack_propagate(False)
lf2.place(x=0, y=180)

text_pos = Text(lf1, font='arial 20 bold', fg='gray25', bg='light gray')
text_pos.pack()
text_pos2 = Text(lf2, font='arial 12 bold', fg='gray25', bg='light gray')
text_pos2.pack()

lb = Label(root, text="Палитра цветов")
lb.configure(fg='navy')
lb.place(x=15, y=275)

btn_1 = Button(root, text="Очистить", font='arial 16 bold',
               bg='gray25', fg='white', bd=20)  # borderwidth = bd
btn_1.place(x=130, y=8)
btn_1.bind("<Button-1>", clean)

btn_2 = Button(root, text='Выбор цвета')
btn_2.configure(font='times 12 bold', width=12, bg='gray25', fg='white', bd=5)
btn_2.place(x=3, y=300)
btn_2.bind("<Button-1>", color_all)

btn_3 = Button(root, text='Красный')
btn_3.configure(font='times 12 bold', width=13, bg='red', fg='white')
btn_3.place(x=2, y=340)
btn_3.bind("<Button-1>", color_red)

btn_4 = Button(root, text='Зеленый')
btn_4.configure(font='times 12 bold', width=13, bg='green', fg='white')
btn_4.place(x=2, y=375)
btn_4.bind("<Button-1>", color_green)

btn_5 = Button(root, text='Синий')
btn_5.configure(font='times 12 bold', width=13, bg='blue', fg='white')
btn_5.place(x=2, y=410)
btn_5.bind("<Button-1>", color_blue)

btn_6 = Button(root, text='Черный')
btn_6.configure(font='times 12 bold', width=13, bg='black', fg='white')
btn_6.place(x=2, y=445)
btn_6.bind("<Button-1>", color_black)

btn_7 = Button(root, text='Ластик')
btn_7.configure(font='times 12 bold', width=13, bg='white', fg='black')
btn_7.place(x=2, y=480)
btn_7.bind("<Button-1>", lastik)

var = IntVar()
var.set(5)
for i in range(6):
    Radiobutton(root, text='scroll' if i == 5 else (i + 1) * 10, variable=var,
                value=i).place(x=310 + i * 40, y=5)

var2 = IntVar()
var2.set(0)
tx = ['mix', 'oval', 'line']
for j in range(len(tx)):
    Radiobutton(root, text=tx[j], variable=var2,
                value=j).place(x=10, y=515 + j * 20)

sc = Scale(root, orient=HORIZONTAL, length=234, from_=0, to=100,
           tickinterval=10, resolution=1, relief=SUNKEN, command=set_size)
sc.set(3)
sc.place(x=315, y=30)

lf3 = LabelFrame(root, text=' Часы ', width=180, height=90, bd=5)
lf3.pack_propagate(False)
lf3.place(x=590, y=0)

lb1 = Label(lf3, font='arial 30')
lb1.place(relx=0, rely=0.1)
lb1.after_idle(tick)

pb = ttk.Progressbar(root, length=800)
pb.pack(side='bottom')  # низ
pb.start(1000)

'''img_label = PhotoImage(file='img/label.png')
lb2 = Label(root, image=img_label)
lb2.place(x=1, y=1, width=110, height=80)'''

try:
    img_btn_fill = PhotoImage(file='img/img1.png')
    btn_8 = Button(root, image=img_btn_fill)
except TclError:
    btn_8 = Button(root, text='fill', font='times 16 bold')
btn_8.place(x=70, y=525)
btn_8.bind('<Button-1>', activate_fill)

canvas.bind('<Button-1>', activate_paint)

root.mainloop()
