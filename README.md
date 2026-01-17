SECRET-INFORMATION-STORING Image Steganography Using Python and tkinter Steganography project with gui. Hides text inside image. Least Significant Algorithm (LSB) is used to hide the text. What is Steganography ? Steganography is the practice of concealing a file, message, image, or video within another file, message, image, or video.

Here in this code we give image and text to be concealed in an image and press Encode. To retrieve the data press Decode. def main(self,root): root.title('SECRET INFORMATION STORING SYSTEM') root.geometry('500x800') # root.resizable(width =False, height=False) f = Frame(root)
title = Label(f,text='SECRET INFORMATION \n STORING SYSTEM',bg="light blue")
title.config(font=('courier',33))
title.grid(pady=10)

b_encode = Button(f,text="Encode",command= lambda :self.frame1_encode(f), padx=14,bg="green")
b_encode.config(font=('courier',14))
b_decode = Button(f, text="Decode",padx=14,command=lambda :self.frame1_decode(f),bg="pink")
b_decode.config(font=('courier',14))
b_decode.grid(pady = 12)

ascii_art = Label(f,text=self.art)
# ascii_art.config(font=('MingLiU-ExtB',50))
ascii_art.config(font=('courier',60))

ascii_art2 = Label(f,text=self.art2)
# ascii_art.config(font=('MingLiU-ExtB',50))
ascii_art2.config(font=('courier',12,'bold'))

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
def home(self,frame): frame.destroy() self.main(root)

def frame1_decode(self,f): f.destroy() d_f2 = Frame(root) label_art = Label(d_f2, text='٩(^‿^)۶') label_art.config(font=('courier',90)) label_art.grid(row =1,pady=50) l1 = Label(d_f2, text='Select Image with Hidden text:') l1.config(font=('courier',18)) l1.grid() bws_button = Button(d_f2, text='Select', command=lambda :self.frame2_decode(d_f2),bg="light green") bws_button.config(font=('courier',18)) bws_button.grid() back_button = Button(d_f2, text='Cancel', command=lambda : Stegno.home(self,d_f2),bg="light blue") back_button.config(font=('courier',18)) back_button.grid(pady=15) back_button.grid() d_f2.grid()

Encode Preview:

f.grid()
title.grid(row=1)
b_encode.grid(row=2)

Here is the program for Decoding :

def decode(self, image):
data = ''
imgdata = iter(image.getdata())
while (True):
    pixels = [value for value in imgdata.__next__()[:3] +
              imgdata.__next__()[:3] +
              imgdata.__next__()[:3]]
    binstr = ''
    for i in pixels[:8]:
        if i % 2 == 0:
            binstr += '0'
        else:
            binstr += '1'
    data += chr(int(binstr, 2))
    if pixels[-1] % 2 != 0:
        return data       
Requirements:- Python tkinter Pillow PIL

How to run? pip install Pillow==7.2.0 pip install tk==0.1.0 python ImageS.py

b_decode.grid(row=3)
ascii_art.grid(row=4,pady=10)
ascii_art2.grid(row=5,pady=5)
