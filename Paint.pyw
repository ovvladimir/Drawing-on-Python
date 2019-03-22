from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
# ImageGrab for Windows
from PIL import Image, ImageTk, ImageDraw, ImageGrab, ImageFont
import math

canvas_width = 700
canvas_height = 500

size = 1
color = '#000000'
rgb = (0, 0, 0)
fill_activate = False
lastik = False
sel = False
im = None
figure = None
font1 = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 150)

lst = ['Черный', 'Красный', 'Зеленый', 'Голубой', 'Желтый', 'Белый',
       'Выбор цвета',
       color,
       'white', 'yellow', 'blue', 'green', 'red', 'black']
tx = ['TEXT', 'oval', 'mix', 'line', 'Квадрат', 'Эллипс', 'Треугольник', 'Линия']

root = Tk()
root.geometry('+1+1')
root.iconphoto(True, PhotoImage(file='img/ico.png'))
root.title('Paint Python')


def activate():
    global fill_activate, lastik
    if sel is True:
        w.tag_unbind(CURRENT, '<B1-Motion>')
        clear()
    w.unbind('<B1-Motion>')
    w.bind('<Button-1>', activate_paint)
    w.bind('<Button-3>', mouse_right)
    btn_brush.configure(relief=SUNKEN, state=DISABLED)
    btn_fill.configure(relief=RAISED, state=NORMAL)
    btn_clear.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    fill_activate = False
    lastik = False


def activate_paint(e):
    global x1, y1, figure
    x1, y1 = e.x, e.y

    if 3 < var.get() < 7:
        w.bind('<B1-Motion>', paint_oval)
    elif var.get() == 7:
        figure = None
        w.unbind('<B1-Motion>')
        w.bind('<Button-1>', paint_line)
    else:
        figure = None
        settings()
        if var.get() == 1:
            w.bind('<B1-Motion>', paint_oval)
        elif var.get() == 3:
            w.bind('<B1-Motion>', paint_line)
        elif var.get() == 2:
            if size > 1:
                w.bind('<B1-Motion>', paint_line, add="+")
                w.bind('<B1-Motion>', paint_oval, add="+")
            else:
                w.bind('<B1-Motion>', paint_line)


def settings():
    global size, color, rgb, rgba

    if size != scl.get():
        for obj in list_btnSize:
            obj.configure(relief=RAISED, state=NORMAL)
    size = scl.get()
    if size == 0:
        scl.set(1)

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
    if var.get() == 7:
        settings()
    x2, y2 = e.x, e.y
    w.create_line((x1, y1, x2, y2), width=size, fill=color, tag='im_id')
    draw.line((x1, y1, x2, y2), width=size, fill=rgba)
    x1, y1 = x2, y2


def paint_oval(e):
    global w_figure, h_figure, h_polygon
    x, y = e.x, e.y
    r = size // 2
    size_figure = x - x1

    if figure == 4:
        clear()
        w.create_rectangle((x1, y1, x, y), fill=color, outline='', tag='im_id')
        draw.rectangle((x1, y1, x, y), fill=rgba, outline=rgba)
    elif figure == 5:
        clear()
        if x >= x1 and y >= y1:  # условие для draw.ellipse
            w.create_oval((x1, y1, x, y), fill=color, outline='', tag='im_id')
            draw.ellipse((x1, y1, x, y), fill=rgba, outline=rgba)
        elif x1 >= x and y1 >= y:
            w.create_oval((x, y, x1, y1), fill=color, outline='', tag='im_id')
            draw.ellipse((x, y, x1, y1), fill=rgba, outline=rgba)
        elif x >= x1 and y1 >= y:
            w.create_oval((x1, y, x, y1), fill=color, outline='', tag='im_id')
            draw.ellipse((x1, y, x, y1), fill=rgba, outline=rgba)
        elif x1 >= x and y >= y1:
            w.create_oval((x, y1, x1, y), fill=color, outline='', tag='im_id')
            draw.ellipse((x, y1, x1, y), fill=rgba, outline=rgba)
    elif figure == 6:
        clear()
        y = y1
        x3 = x1+size_figure*math.cos(45)
        y3 = y1+size_figure*math.sin(45)
        w.create_polygon((x1, y1, x3, y3, x, y), fill=color, outline='', tag='im_id')
        draw.polygon((x1, y1, x3, y3, x, y), fill=rgba, outline=rgba)
    else:
        w.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='', tag='im_id')
        draw.ellipse((x-r, y-r, x+r, y+r), fill=rgba, outline=rgba)

    w_figure = (x - x1)/2
    h_figure = (y - y1)/2
    h_polygon = (size_figure*math.sqrt(3)/2)/2
    if 3 < var.get() < 7:
        settings()


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


def activate_fill():
    global fill_activate, lastik, figure
    if sel is True:
        w.tag_unbind(CURRENT, '<B1-Motion>')
        clear()
    fill_activate = True
    lastik = False
    figure = None
    btn_fill.configure(relief=SUNKEN, state=DISABLED)
    btn_brush.configure(relief=RAISED, state=NORMAL)
    btn_clear.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    w.unbind('<B1-Motion>')
    w.bind('<Button-1>', fill_)


def fill_(e):
    global image_tk, im
    settings()
    xf, yf = e.x, e.y
    if fill_activate is True:
        ImageDraw.floodfill(imag, xy=(xf, yf), value=rgba)
        image_tk = ImageTk.PhotoImage(image=imag)
        im = w.create_image(0, 0, anchor=NW, image=image_tk)
        w.delete('txt_id')
        '''im1 = w.create_image(w.coords(im), anchor=NW, image=image_tk)
        # w.coords(im) координаты im
        w.delete(im)
        im = im1'''


def activate_lastik(new_col=lst[-6]):
    global fill_activate, lastik, figure
    btn_clear.configure(relief=SUNKEN, state=DISABLED)
    btn_fill.configure(relief=RAISED, state=NORMAL)
    btn_brush.configure(relief=RAISED, state=NORMAL)
    btn_select.configure(relief=RAISED, state=NORMAL)
    if sel is True:
        w.tag_unbind(im, '<B1-Motion>')
        clear()
    lastik = True
    fill_activate = False
    figure = None
    var.set(2)
    w.bind('<Button-1>', activate_paint)
    return color_change(new_col)


def clear():
    global imag, draw, im, sel

    w.delete("all")
    text_rgb.delete(1.0, END)

    imag.close()
    imag = Image.new('RGBA', (canvas_width+20, canvas_height))
    draw = ImageDraw.Draw(imag)

    im = None
    sel = False


def new_file():
    clear()


def open_file():
    global image_tk, im
    try:
        file_name = fd.askopenfilename()
        image2 = Image.open(file_name)
        image2_w, image2_h = image2.size
        imag_w, imag_h = imag.size
        set_size = ((imag_w - image2_w) // 2, (imag_h - image2_h) // 2)
        print(image2.mode)
        if image2.mode == 'RGBA':
            imag.alpha_composite(image2, set_size)
        elif image2.mode == 'RGB':
            # a_channel = Image.new('L', image2.size, 255)
            # image2.putalpha(a_channel)  # добавление альфа-канала к image2
            imag.paste(image2, set_size)
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
    top.minsize(width=230, height=100)
    label_about = Label(top, text='Это самое лучшее \nприложение для рисования',
                        fg='red')
    label_about.pack()


def mouse_right(e):
    menu_right.post(e.x_root, e.y_root)


def entry_text():
    global entry, top2
    top2 = Toplevel()
    top2.minsize(width=150, height=100)
    lb_txt = Label(top2, text='Введите текст')
    lb_txt.pack()
    entry = Entry(top2)
    entry.focus()
    entry.pack(pady=5)
    Button(top2, text='Напечатать?', bd=15, command=image_text).pack()


def image_text():
    global image_txt, im
    w.delete('im_id')
    w.delete('txt_id')
    w.delete(im)
    entry_txt = entry.get()
    top2.destroy()

    settings()
    w_txt, h_txt = draw.textsize(entry_txt, font=font1)
    draw.text(((canvas_width-w_txt)/2, (canvas_height-h_txt)/2),
              entry_txt, fill=rgba, font=font1)
    image_txt = ImageTk.PhotoImage(image=imag)
    im = w.create_image(0, 0, anchor=NW, image=image_txt, tag='txt_id')


def select():
    global fill_activate, lastik, sel, im
    if im is not None or figure is not None:
        sel = True
        lastik = False
        fill_activate = False
        btn_select.configure(relief=SUNKEN, state=DISABLED)
        btn_clear.configure(relief=RAISED, state=NORMAL)
        btn_fill.configure(relief=RAISED, state=NORMAL)
        btn_brush.configure(relief=RAISED, state=NORMAL)
        w.unbind('<Button-1>')
        w.unbind('<B1-Motion>')
        w.tag_bind(CURRENT, "<B1-Motion>", change_img)
        if im is not None:
            w.delete('im_id')


def change_img(e):
    # CURRENT - текущий элемент под мышью
    imag_w, imag_h = imag.size
    if figure == 4 or figure == 5:
        w.coords(CURRENT, (e.x-w_figure, e.y-h_figure, e.x+w_figure, e.y+h_figure))
    elif figure == 6:
        w.coords(CURRENT, (e.x-w_figure, e.y-h_polygon,
                           e.x, e.y+h_polygon,
                           e.x+w_figure, e.y-h_polygon))
    else:
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
for n in range(len(tx)):
    def figures(f=n):
        global figure
        var.set(f)
        figure = f
        activate()
    menu_right.add_command(label='TEXT' if n == 0 else tx[n],
                           command=entry_text if n == 0 else figures)
    menu_right.add_separator() if n == 0 or n == 3 else None

w = Canvas(root, width=canvas_width, height=canvas_height,
           bg='white', cursor='spider', relief=SUNKEN)
w.grid(row=2, column=0, columnspan=6, padx=3, pady=3, sticky=E + W + S + N)

imag = Image.new('RGBA', (canvas_width+20, canvas_height))
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
var.set(2)
for j in range(1, len(tx)//2):
    Radiobutton(root, text=tx[j], variable=var, fg='navy', value=j,
                command=activate).place(x=740+(j-1)*25, y=520 if j == 2 else 500)

img_btn_brush = PhotoImage(file='img/img0.png')
btn_brush = Button(root, image=img_btn_brush, command=activate)
btn_brush.configure(relief=SUNKEN, state=DISABLED)
btn_brush.place(x=797, y=254)
img_btn_fill = PhotoImage(file='img/img1.png')
btn_fill = Button(root, image=img_btn_fill, command=activate_fill)
btn_fill.place(x=797, y=304)
img_btn_clear = PhotoImage(file='img/img2.png')
btn_clear = Button(root, image=img_btn_clear, command=activate_lastik)
btn_clear.place(x=797, y=354)
img_btn_color = PhotoImage(file='img/img3.png')
btn_color = Button(root, image=img_btn_color, command=color_all)
btn_color.place(x=797, y=404)
btn_select = Button(root, text='↖', font='calibri 10 bold', width=6, bd=4,
                    command=select)
btn_select.place(x=797, y=458)

activate()
root.mainloop()
