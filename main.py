from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2
import numpy

class GUI:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.label = Label(frame, text="This is our first GUI!")
        self.label.pack()

        self.select_scene_btn = Button(frame, text="Select scene", command=lambda: self.displayImage("scene"),
                                       padx="5", pady="5", width="10")
        self.select_scene_btn.pack()

        self.select_sprite_btn = Button(frame, text="Select sprite", command=lambda: self.displayImage("sprite"),
                                        padx="5", pady="5", width="10")
        self.select_sprite_btn.pack()

        self.close_button = Button(frame, text="Close", command=frame.quit,
                                   padx="5", pady="5", width="10")
        self.close_button.pack()

        self.sceneCanvas = Canvas(root)
        self.spriteCanvas = Canvas(root)


    def displayImage(self, identifier):
        self.imgPath = filedialog.askopenfilename()
        if identifier == "scene":
            self.scenePhoto = ImageTk.PhotoImage(Image.open(self.imgPath))
            self.sceneCanvas.create_image((0, 0), image=self.scenePhoto, anchor="nw")
            self.sceneCanvas.image = self.scenePhoto
            self.sceneCanvas.pack()

        else:
            self.spritePhoto = ImageTk.PhotoImage(Image.open(self.imgPath))
            self.spriteCanvas.create_image((0, 0), image=self.spritePhoto, anchor="nw")
            self.spriteCanvas.image = self.spritePhoto
            self.spriteCanvas.pack()

        # return self.imgPath if len(self.imgPath) > 0 else "No image selected"


root = Tk()
my_gui = GUI(root)
root.mainloop()