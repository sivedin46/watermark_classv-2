from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os


class Watermark:
    def __init__(self):
        self.font_palette = ["black", "white", "red", "blue", "brown", "yellow", "green", "grey", "pink"]
        self.color = ()
        self.button_count = 1  # actually we can create this in create_color_button method
        self.picture = None
        self.result = None

        self.window = Tk()
        self.window.title("Apply Watermark")
        self.window.config(padx=20, pady=20, bg="white")
        self.i = PhotoImage(width=1, height=1)

        # Create UI components
        self.create_ui_components()
        self.create_color_buttons(self.font_border_frame)
        self.window.mainloop()

    def create_ui_components(self):
        # Create font palette frame and buttons
        self.font_palette_frame = Frame(self.window)
        self.font_palette_frame.pack(anchor="center")
        font_color_label = Label(self.font_palette_frame, text="Font Palette")
        font_color_label.pack(side="top")
        self.font_border_frame = Frame(self.window)
        self.font_border_frame.pack(anchor="center")

        # Create entry frame
        self.entry_frame = Frame(self.window)
        self.entry_frame.pack(side="top", fill="x", pady=10)
        watermark_text_label = Label(self.entry_frame, text="Watermark Text")
        watermark_text_label.pack(side="left", padx=5)
        self.text_entry = Entry(self.entry_frame, width=35)
        self.text_entry.pack(side="left", padx=5)
        self.file_entry = Entry(self.entry_frame, width=35)
        self.file_entry.pack(side="left", padx=5)
        file_open_label = Label(self.entry_frame, text="File Path:")
        file_open_label.pack(side="left", padx=5)
        open_file_button = Button(self.entry_frame, width=14, text="Select Picture",
                                  command=lambda: self.open_picture(self.file_entry, self.x_position_button,
                                                                    self.y_position_button))
        open_file_button.pack(side="left", padx=5)

        # Create button frame
        self.button_frame = Frame(self.window)
        self.button_frame.pack(side="bottom", fill="x", pady=10)
        save_button = Button(self.button_frame, width=33, text="Save", command=self.save_file)
        save_button.pack(side="right", padx=5)
        converter_button = Button(self.button_frame, width=33, text="Convert",
                                  command=lambda: self.converter(self.font_button, self.opacity_button, self.text_entry,
                                                                 self.x_position_button, self.y_position_button))
        converter_button.pack(side="right", padx=5)

        # Create slider frame
        self.slider_frame = Frame(self.window)
        self.slider_frame.pack(side="bottom", fill="x", pady=10)
        opacity_label = Label(self.slider_frame, text="Opacity")
        opacity_label.pack(side="left", padx=5)
        self.opacity_button = Scale(self.slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
        self.opacity_button.pack(side="left", padx=5)
        font_label = Label(self.slider_frame, text="Font")
        font_label.pack(side="left", padx=5)
        self.font_button = Scale(self.slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
        self.font_button.pack(side="left", padx=5)
        x_position_button_label = Label(self.slider_frame, text="X Pos.")
        x_position_button_label.pack(side="left", padx=5)
        self.x_position_button = Scale(self.slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
        self.x_position_button.pack(side="left", padx=5)
        y_position_button_label = Label(self.slider_frame, text="Y Pos.")
        y_position_button_label.pack(side="left", padx=5)
        self.y_position_button = Scale(self.slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
        self.y_position_button.pack(side="left", padx=5)

    def create_color_buttons(self, font_border_frame):
        for index in range(9):
            button_id = self.button_count
            button = Button(font_border_frame,
                            bd=0,
                            relief="flat",
                            borderwidth=0,
                            bg=f"{self.font_palette[self.button_count - 1]}",
                            activebackground=f"{self.font_palette[self.button_count - 1]}",
                            font=('arial', 80, 'bold'),
                            compound='bottom',
                            anchor="center",
                            width=20,
                            height=20,
                            image=self.i)
            button.pack(side="left", padx=1, pady=1)
            button.config(command=lambda b_id=button_id: self.select_color(b_id))
            self.button_count += 1

    def open_picture(self, file_entry, x_position_button, y_position_button):
        file_path = filedialog.askopenfilename(title="Open Image File",
                                               filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            file_entry.delete(0, END)  # clear entry
            file_entry.insert(index=0, string=file_path)
            self.picture = Image.open(file_path).convert("RGBA")
            x_size = self.picture.size[0]
            y_size = self.picture.size[1]
            x_position_button.configure(from_=0, to=x_size)
            y_position_button.configure(from_=0, to=y_size)
        else:
            messagebox.showinfo(title="Warning", message="No file selected")

    def converter(self, font_button, opacity_button, text_entry, x_position_button, y_position_button):
        if not self.picture:
            messagebox.showinfo(title="Warning", message="No picture selected")
            return
        template = Image.new("RGBA", self.picture.size, (255, 255, 255, 0))  # making transparent template
        text_font = font_button.get()
        if text_font == 0:
            messagebox.showinfo(title="Warning", message="Text Font must be bigger then zero")
            return
        fnt = ImageFont.truetype("TimesNewBastard-ItalicWeb.ttf", text_font)  # font
        draw_text = ImageDraw.Draw(template)  # get a drawing context
        opa_val = opacity_button.get()
        user_text = text_entry.get()
        if not user_text:
            messagebox.showinfo(title="Warning", message="Please enter watermark text")
            return
        if not self.color:
            messagebox.showinfo(title="Warning", message="Please select watermark color")
            return
        fill_color = self.color + (opa_val,)
        x_position = x_position_button.get()
        y_position = y_position_button.get()
        position = (x_position, y_position)

        draw_text.text(position, text=user_text, font=fnt, fill=fill_color)  # opacity(0,255)
        self.result = Image.alpha_composite(self.picture, template)
        self.result.show()

    def select_color(self, but_id):
        self.color = ImageColor.getrgb(self.font_palette[but_id - 1])

    def save_file(self):
        if not self.result:
            messagebox.showinfo(title="Warning", message="No result to save")
            return
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                        filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            abs_path = os.path.abspath(file.name)
            self.result.save(abs_path)


Watermark()
