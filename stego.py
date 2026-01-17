from tkinter import *
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk

class StegnoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Steganography - Modern UI")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        Style(theme="superhero")

        self.sidebar()
        self.header()
        self.main_screen()

    # ------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------
    def sidebar(self):
        self.sidebar_frame = Frame(self.root, bg="#0A0F24", width=180)
        self.sidebar_frame.pack(side=LEFT, fill=Y)

        Label(self.sidebar_frame, text="🔐 StegoTool",
              bg="#0A0F24", fg="white",
              font=("Segoe UI", 16, "bold")).pack(pady=20)

        self.add_sidebar_button("🏠 Home", self.main_screen)
        self.add_sidebar_button("🖼 Encode", self.encode_screen)
        self.add_sidebar_button("📤 Decode", self.decode_screen)
        self.add_sidebar_button("ℹ About", self.about_screen)

    def add_sidebar_button(self, text, cmd):
        btn = Button(self.sidebar_frame, text=text, command=cmd,
                     bg="#141A35", fg="white",
                     activebackground="#1C274A",
                     font=("Segoe UI", 12), bd=0)
        btn.pack(fill=X, pady=5, padx=10, ipady=8)

    # ------------------------------------------------
    # HEADER
    # ------------------------------------------------
    def header(self):
        self.header_frame = Frame(self.root, bg="#10172A", height=60)
        self.header_frame.pack(fill=X)

        Label(self.header_frame, text="Image Steganography Tool",
              font=("Segoe UI", 18, "bold"),
              bg="#10172A", fg="white").pack(pady=12)

    # CLEAR RIGHT SIDE
    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget not in [self.sidebar_frame, self.header_frame]:
                widget.destroy()

    # -------------------------------------------------------------
    # MAIN SCREEN
    # -------------------------------------------------------------
    def main_screen(self):
        self.clear_screen()
        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Welcome to StegoTool",
              font=("Segoe UI", 26, "bold"),
              bg="#192238", fg="white").pack(pady=40)

        Label(frame, text="Embed hidden messages into images securely.",
              font=("Segoe UI", 14),
              bg="#192238", fg="#B7C2F0").pack()

    # -------------------------------------------------------------
    # ENCODE UI
    # -------------------------------------------------------------
    def encode_screen(self):
        self.clear_screen()

        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Encode Message",
              font=("Segoe UI", 22, "bold"),
              bg="#192238", fg="white").pack(pady=20)

        ttk.Button(frame, text="Select Image", bootstyle="primary",
                   command=self.select_encode_image).pack(pady=10)

        self.preview_label = Label(frame, bg="#192238")
        self.preview_label.pack(pady=10)

    def select_encode_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg")]
        )
        if not self.image_path:
            return

        # Show preview
        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)

        self.preview_label.config(image=img)
        self.preview_label.image = img

        self.encode_message_screen()

    def encode_message_screen(self):
        self.clear_screen()

        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Enter Message",
              font=("Segoe UI", 20, "bold"),
              bg="#192238", fg="white").pack(pady=15)

        self.text_box = Text(frame, height=10, width=50, bg="#0F1629", fg="white",
                             insertbackground="white", bd=0)
        self.text_box.pack(pady=10)

        ttk.Button(frame, text="Encode & Save", bootstyle="success",
                   command=self.encode_and_save).pack(pady=20)

    # -------------------------------------------------------------
    # ENCODING LOGIC
    # -------------------------------------------------------------
    def genData(self, data):
        return [format(ord(i), "08b") for i in data]

    def modPix(self, pix, data):
        datalist = self.genData(data)
        imdata = iter(pix)

        for i in range(len(datalist)):
            pixels = [value for value in
                      next(imdata)[:3] +
                      next(imdata)[:3] +
                      next(imdata)[:3]]

            for j in range(8):
                if datalist[i][j] == '0' and pixels[j] % 2 != 0:
                    pixels[j] -= 1
                elif datalist[i][j] == '1' and pixels[j] % 2 == 0:
                    pixels[j] -= 1

            if i == len(datalist) - 1:
                if pixels[-1] % 2 == 0:
                    pixels[-1] -= 1
            else:
                if pixels[-1] % 2 != 0:
                    pixels[-1] -= 1

            yield tuple(pixels[:3])
            yield tuple(pixels[3:6])
            yield tuple(pixels[6:9])

    def encode_and_save(self):
        data = self.text_box.get("1.0", END).strip()
        if not data:
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        image = Image.open(self.image_path)
        new = image.copy()

        w = new.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(image.getdata(), data):
            new.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )

        if save_path:
            new.save(save_path)
            messagebox.showinfo("Success", "Message encoded & saved!")

    # -------------------------------------------------------------
    # DECODE UI + LOGIC
    # -------------------------------------------------------------
    def decode_screen(self):
        self.clear_screen()

        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Decode Message",
              font=("Segoe UI", 22, "bold"),
              bg="#192238", fg="white").pack(pady=20)

        ttk.Button(frame, text="Select Image",
                   bootstyle="info",
                   command=self.decode_image).pack(pady=20)

    def decode_image(self):
        img_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg")]
        )
        if not img_path:
            return

        image = Image.open(img_path)
        data = ""
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in
                      next(imgdata)[:3] +
                      next(imgdata)[:3] +
                      next(imgdata)[:3]]

            binstr = ''.join(['0' if i % 2 == 0 else '1'
                              for i in pixels[:8]])

            data += chr(int(binstr, 2))

            if pixels[-1] % 2 != 0:
                break

        self.show_decoded(data)

    def show_decoded(self, data):
        self.clear_screen()

        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="Decoded Message",
              font=("Segoe UI", 22, "bold"),
              bg="#192238", fg="white").pack(pady=20)

        box = Text(frame, height=10, width=50, bg="#0F1629", fg="white", bd=0)
        box.pack(pady=10)
        box.insert(END, data)
        box.config(state="disabled")

    # -------------------------------------------------------------
    # ABOUT PAGE
    # -------------------------------------------------------------
    def about_screen(self):
        self.clear_screen()

        frame = Frame(self.root, bg="#192238")
        frame.pack(fill=BOTH, expand=True)

        Label(frame, text="About This App",
              font=("Segoe UI", 22, "bold"),
              bg="#192238", fg="white").pack(pady=20)

        Label(frame,
              text="This tool hides secret messages inside images using LSB.\n"
                   "Created by Shawak Gupta\n"
                   "Version: 2.0 (Modern UI)",
              font=("Segoe UI", 14),
              bg="#192238", fg="#B7C2F0").pack(pady=20)


# -------------------------------------
# RUN APP
# -------------------------------------
root = Tk()
StegnoApp(root)
root.mainloop()
