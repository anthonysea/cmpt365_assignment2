from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2
import numpy

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.select_scene_btn = Button(frame, text="Select scene", command=lambda: self.displayImage("scene"),
                                       padx="2", pady="2", width="13")
        self.select_scene_btn.pack(pady="5")

        self.select_sprite_btn = Button(frame, text="Select sprite", command=lambda: self.displayImage("sprite"),
                                        padx="2", pady="2", width="13")
        self.select_sprite_btn.pack(pady="5")

        self.merge_btn = Button(frame, text="Merge", padx="2", pady="2", width="13")
        self.merge_btn.pack(pady="5")

        self.save_btn = Button(frame, text="Save & compress", padx="2", pady="2", width="13")
        self.save_btn.pack(pady="5")

        self.close_button = Button(frame, text="Close", command=frame.quit,
                                   padx="2", pady="2", width="13")
        self.close_button.pack(pady="5")

        self.sceneCanvas = Canvas(root, width=930, height=600)
        self.spriteCanvas = Canvas(root, width=256, height=256)


    def displayImage(self, identifier):
        self.imgPath = filedialog.askopenfilename()
        if identifier == "scene":
            self.sceneImg = Image.open(self.imgPath)
            self.sceneImg.thumbnail((256,256))
            self.scenePhoto = ImageTk.PhotoImage(self.sceneImg)
            self.sceneCanvas.create_image((0, 0), image=self.scenePhoto, anchor="nw")
            self.sceneCanvas.image = self.scenePhoto
            self.sceneCanvas.pack()

        else:
            self.spriteImg = Image.open(self.imgPath)
            self.spriteImg.thumbnail((256,256))
            self.spritePhoto = ImageTk.PhotoImage(Image.open(self.imgPath))
            self.spriteCanvas.create_image((0, 0), image=self.spritePhoto, anchor="nw")
            self.spriteCanvas.image = self.spritePhoto
            self.spriteCanvas.pack()

        # return self.imgPath if len(self.imgPath) > 0 else "No image selected"

    def mergeImages(self):
        """
        Steps to merging scene & sprite
        1. create an image with the size and bg colour you want in RGBA mode
        2. create blank image of the same size in mode "1" to be used as a mask
        3. past the sprite on the mask using ImageDraw module
        4. use Image.paste(colour, box, mask) to paste the colour (0,0,0,0) everywhere the sprite is in the mask
        :return:
        """


root = Tk()
root.resizable(width=True, height=True)
app = App(root)
root.mainloop()