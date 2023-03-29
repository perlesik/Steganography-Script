import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import numpy as np


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.file_name_left = ""
        self.file_name_right = ""
        self.title("Steganografia")

        frame_left = tk.Frame(master=self, width=180, height=210)
        frame_right = tk.Frame(master=self, width=180, height=210)
        frame_left.pack(expand=True, side=tk.LEFT, fill=tk.Y)
        frame_right.pack(expand=True, side=tk.RIGHT, fill=tk.Y)

        # LEFT FRAME
        desc_label = tk.Label(text="ZASZYFRUJ", master=frame_left)
        desc_label.place(x=5, y=3)
        open_button = tk.Button(master=frame_left, text="Wybierz plik", command=lambda: self.select_file("left"))
        open_button.place(x=5, y=25)
        show_image_button = tk.Button(master=frame_left, text="Pokaż zdjęcie",
                                      command=lambda: self.show_image("left"))
        show_image_button.place(x=5, y=55)

        self.column_var = tk.IntVar()
        column_label = tk.Label(text="Kolumna", master=frame_left)
        column_label.place(x=5, y=85)
        self.column_entry = tk.Entry(textvariable=self.column_var, width=5, master=frame_left)
        self.column_entry.place(x=5, y=105)

        self.row_var = tk.IntVar()
        row_label = tk.Label(text="Wiersz", master=frame_left)
        row_label.place(x=65, y=85)
        self.row_entry = tk.Entry(textvariable=self.row_var, width=5, master=frame_left)
        self.row_entry.place(x=65, y=105)

        self.text_var = tk.StringVar()
        text_label = tk.Label(text="Tekst do ukrycia", master=frame_left)
        text_label.place(x=5, y=125)
        self.text_entry = tk.Entry(textvariable=self.text_var)
        self.text_entry.place(x=5, y=145)

        encode_button = tk.Button(master=frame_left, text="Zaszyfruj", command=self.encode)
        encode_button.place(x=5, y=175)

        # RIGHT FRAME
        desc2_label = tk.Label(text="ODSZYFRUJ", master=frame_right)
        desc2_label.place(x=5, y=3)
        open2_button = tk.Button(master=frame_right, text="Wybierz plik", command=lambda: self.select_file("right"))
        open2_button.place(x=5, y=25)
        show2_image_button = tk.Button(master=frame_right, text="Pokaż zdjęcie",
                                       command=lambda: self.show_image("right"))
        show2_image_button.place(x=5, y=55)

        self.column2_var = tk.IntVar()
        column2_label = tk.Label(text="Kolumna", master=frame_right)
        column2_label.place(x=5, y=85)
        self.column2_entry = tk.Entry(textvariable=self.column2_var, width=5, master=frame_right)
        self.column2_entry.place(x=5, y=105)

        self.row2_var = tk.IntVar()
        row2_label = tk.Label(text="Wiersz", master=frame_right)
        row2_label.place(x=65, y=85)
        self.row2_entry = tk.Entry(textvariable=self.row2_var, width=5, master=frame_right)
        self.row2_entry.place(x=65, y=105)

        self.count_var = tk.IntVar()
        count_label = tk.Label(text="Znaki", master=frame_right)
        count_label.place(x=125, y=85)
        self.count_entry = tk.Entry(textvariable=self.count_var, width=5, master=frame_right)
        self.count_entry.place(x=125, y=105)

        text2_label = tk.Label(text="Odszyfrowany tekst", master=frame_right)
        text2_label.place(x=5, y=125)
        self.decoded_label = tk.Label(text="[ tekst ]", master=frame_right)
        self.decoded_label.place(x=5, y=142)

        decode_button = tk.Button(master=frame_right, text="Odszyfruj", command=self.decode)
        decode_button.place(x=5, y=175)

    def select_file(self, side):
        file_types = (('bmp files', '*.bmp'), ('All files', '*.*'))
        if side == "left":
            self.file_name_left = fd.askopenfilename(title="Wybierz plik", initialdir="/", filetypes=file_types)
        else:
            self.file_name_right = fd.askopenfilename(title="Wybierz plik", initialdir="/", filetypes=file_types)
        # self.show_image()

    def show_image(self, side):
        if side == "left" and self.file_name_left == "":
            return
        if side == "right" and self.file_name_right == "":
            return

        photo_window = tk.Toplevel(master=self)
        photo_window.title("Wybrane zdjęcie")

        frame = tk.Frame(master=photo_window, width=400, height=400)
        frame.pack(expand=True, side=tk.TOP)

        if side == "left":
            img = Image.open(self.file_name_left)
        else:
            img = Image.open(self.file_name_right)
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(master=frame, image=img_tk)
        img_label.image = img_tk
        img_label.pack(side="bottom")

    def save_new_file(self, img):
        file_types = (('bmp files', '*.bmp'), ('All files', '*.*'))
        file_name = fd.asksaveasfile(mode='wb', defaultextension=".bmp", filetypes=file_types)
        if file_name is None:
            return
        img.save(file_name)
        mb.showinfo(title="Komunikat", message="Plik został pomyślnie zapisany!")

    def encode(self):
        img = Image.open(self.file_name_left)
        img_data = list(img.getdata())
        arr = np.array(img_data)
        arr_2d = np.reshape(arr, (img.height, img.width))
        row = self.row_var.get()
        column = self.column_var.get()
        for count, char in enumerate(self.text_var.get()):
            arr_2d[row * count][column * count] = ord(char)
            # print(f"{char} = {ord(char)}")
        img_new = Image.fromarray(np.uint8(arr_2d), mode="L")
        # img_new.show()
        self.save_new_file(img_new)

    def decode(self):
        text = ""
        img = Image.open(self.file_name_right)
        img_data = list(img.getdata())
        arr = np.array(img_data)
        arr_2d = np.reshape(arr, (img.height, img.width))
        row = self.row2_var.get()
        column = self.column2_var.get()
        for i in range(self.count_var.get()):
            text += chr(arr_2d[row * i][column * i])
        self.decoded_label.config(text=text)


if __name__ == '__main__':
    app = App()
    app.mainloop()
