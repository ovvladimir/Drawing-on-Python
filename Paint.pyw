from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
# ImageGrab for Windows
from PIL import Image, ImageTk, ImageDraw, ImageGrab, ImageFont

canvas_width = 700
canvas_height = 500

size = 1
color = '#000000'
rgb = (0, 0, 0)
fill_activate = False
lastik = False
sel = False
im = None

lst = ['Черный', 'Красный', 'Зеленый', 'Голубой', 'Желтый', 'Белый',
       'Выбор цвета',
       color,
       'white', 'yellow', 'blue', 'green', 'red', 'black']

root = Tk()
root.title("Paint Python")
root.geometry('+1+1')


def activate():
    global fill_activate, lastik
    if sel is True:
        w.tag_unbind(im, '<B1-Motion>')
        clear()
    w.bind('<Button-1>', activate_paint)
    w.bind('<Button-3>', mouse_right)
    btn_brush.configure(relief=SUNKEN, state=DISABLED)
    btn_fill.configure(relief=RAISED, state=NORMAL)
    btn_clear.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    fill_activate = False
    lastik = False


def activate_paint(e):
    global x1, y1, size
    x1, y1 = e.x, e.y

    if size != scl.get():
        for obj in list_btnSize:
            obj.configure(relief=RAISED, state=NORMAL)

    size = scl.get()
    if size == 0:
        scl.set(1)
    txt()

    if var.get() == 0:
        w.bind('<B1-Motion>', paint_oval)
    elif var.get() == 2:
        w.bind('<B1-Motion>', paint_line)
    else:
        if size > 1:
            w.bind('<B1-Motion>', paint_line, add="+")
            w.bind('<B1-Motion>', paint_oval, add="+")
        else:
            w.bind('<B1-Motion>', paint_line)


def txt():
    global rgb, color, rgba
    color = lstBox.get(lstBox.curselection())
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

    if lastik is False:
        rgba = int(rgb[0]), int(rgb[1]), int(rgb[2]), 255
    else:
        rgba = int(rgb[0]), int(rgb[1]), int(rgb[2]), 0

    text_rgb.delete(1.0, END)
    text_rgb.insert(1.0, f' {color} \n {int(rgb[0]), int(rgb[1]), int(rgb[2])}')


def paint_line(e):
    global x1, y1
    x2, y2 = e.x, e.y
    w.create_line((x1, y1, x2, y2), width=size, fill=color, tag='im_id')
    draw.line((x1, y1, x2, y2), width=size, fill=rgba)
    x1, y1 = x2, y2


def paint_oval(e):
    x, y = e.x, e.y
    r = size // 2
    w.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='', tag='im_id')
    draw.ellipse((x-r, y-r, x+r, y+r), fill=rgba, outline=rgba)


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


def activate_fill(e):
    global fill_activate, lastik
    if sel is True:
        w.tag_unbind(im, '<B1-Motion>')
        clear()
    fill_activate = True
    lastik = False
    btn_fill.configure(relief=SUNKEN, state=DISABLED)
    btn_brush.configure(relief=RAISED, state=NORMAL)
    btn_clear.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    w.bind('<Button-1>', fill_, add='+')


def fill_(e):
    global image_tk, im
    txt()
    xf, yf = e.x, e.y
    if fill_activate is True:
        # заливка изображение
        ImageDraw.floodfill(imag, xy=(xf, yf), value=rgba)
        # рисуем на холсте
        image_tk = ImageTk.PhotoImage(image=imag)
        im = w.create_image(0, 0, anchor=NW, image=image_tk)
        '''im1 = w.create_image(w.coords(im), anchor=NW, image=image_tk)
        # w.coords(im) координаты im
        w.delete(im)
        im = im1'''


def activate_lastik(new_col=lst[-6]):
    global fill_activate, lastik
    btn_clear.configure(relief=SUNKEN, state=DISABLED)
    btn_fill.configure(relief=RAISED, state=NORMAL)
    btn_brush.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    if sel is True:
        w.tag_unbind(im, '<B1-Motion>')
        clear()
    lastik = True
    fill_activate = False
    return color_change(new_col)


def clear():
    global imag, draw, im, sel

    w.delete("all")
    text_rgb.delete(1.0, END)

    imag.close()
    imag = Image.new('RGBA', (canvas_width, canvas_height))
    draw = ImageDraw.Draw(imag)

    im = None
    sel = False


def new_file():
    clear()


def open_file():
    global imag, image_tk, im
    try:
        file_name = fd.askopenfilename()
        image2 = Image.open(file_name)
        image2_w, image2_h = image2.size
        imag_w, imag_h = imag.size
        set_size = ((imag_w - image2_w) // 2, (imag_h - image2_h) // 2)
        imag.alpha_composite(image2, set_size)
        # imag.paste(image2, set_size)
        image_tk = ImageTk.PhotoImage(image=imag)
        im = w.create_image(0, 0, anchor=NW, image=image_tk)
    except (FileNotFoundError, ValueError, AttributeError, TclError):
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


def save_file2():
    try:
        file_name = fd.asksaveasfilename(defaultextension='.png',
                                         filetypes=(('PNG files', '*.png'),
                                                    ('All files', '*.*')))
        imag.save(file_name)
    except (FileNotFoundError, ValueError):
        pass


def about():
    top = Toplevel()
    top.title('About')
    top.minsize(width=200, height=100)
    label_about = Label(top, text='Лучшее приложение для рисования', fg='red')
    label_about.pack()


def mouse_right(e):
    global x, y
    x, y = e.x, e.y
    menu_right.post(e.x_root, e.y_root)


def text():
    global image_txt, im
    draw.text((0, 0), 'PAINT', fill=rgb,
              font=ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 150))
    image_txt = ImageTk.PhotoImage(image=imag)
    w.delete(im)
    im = w.create_image(0, 0, anchor=NW, image=image_txt)


def select():
    global fill_activate, lastik, sel, im
    if im is not None:
        sel = True
        lastik = False
        fill_activate = False
        btn_select.configure(relief=SUNKEN, state=DISABLED)
        btn_clear.configure(relief=RAISED, state=NORMAL)
        btn_fill.configure(relief=RAISED, state=NORMAL)
        btn_brush.configure(relief=RAISED, state=NORMAL)
        w.delete('im_id')
        w.unbind('<Button-1>')
        w.unbind('<B1-Motion>')
        w.tag_bind(im, "<B1-Motion>", change_img)


def change_img(e):
    imag_w, imag_h = imag.size
    # im или CURRENT - текущий элемент под мышью
    w.coords(im, (e.x-imag_w/2, e.y-imag_h/2))


filemenu = Menu(root)
root.config(menu=filemenu)
submenu = Menu(filemenu, tearoff=0)
helpmenu = Menu(filemenu, tearoff=0)
submenu.add_command(label="Новый", command=new_file)
submenu.add_command(label="Открыть", command=open_file)
submenu.add_command(label="Сохранить RGB", command=save_file)
submenu.add_command(label="Сохранить RGBA", command=save_file2)
submenu.add_separator()
submenu.add_command(label="Выход", command=root.destroy)
helpmenu.add_command(label="О программе", command=about)
filemenu.add_cascade(label="Файл", menu=submenu)
filemenu.add_cascade(label="Справка", menu=helpmenu)

menu_right = Menu(tearoff=0)
menu_right.add_command(label='Text', command=text)

w = Canvas(root, width=canvas_width, height=canvas_height,
           bg='white', cursor='spider')
w.grid(row=2, column=0, columnspan=6, padx=3, pady=3, sticky=E + W + S + N)

imag = Image.new('RGBA', (canvas_width, canvas_height))
draw = ImageDraw.Draw(imag)

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

img_btn_brush = PhotoImage(file='img/img0.png')
btn_brush = Button(root, image=img_btn_brush, command=activate)
btn_brush.configure(relief=SUNKEN, state=DISABLED)
btn_brush.place(x=797, y=254)
img_btn_fill = PhotoImage(file='img/img1.png')
btn_fill = Button(root, image=img_btn_fill)
btn_fill.place(x=797, y=304)
btn_fill.bind('<Button-1>', activate_fill)
img_btn_clear = PhotoImage(file='img/img2.png')
btn_clear = Button(root, image=img_btn_clear, command=activate_lastik)
btn_clear.place(x=797, y=354)
img_btn_color = PhotoImage(file='img/img3.png')
btn_color = Button(root, image=img_btn_color, command=color_all)
btn_color.place(x=797, y=404)
btn_select = Button(root, text='↖', font='calibri 11 bold', width=5, bd=4,
                    command=select)
btn_select.place(x=797, y=457)

activate()
root.mainloop()
