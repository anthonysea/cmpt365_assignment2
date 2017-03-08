from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2
import numpy

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.select_scene_btn = Button(master, text="Select scene", command=self.getImagePath)
        self.select_scene_btn.pack()

        self.select_sprite_btn = Button(master, text="Select sprite", command=self.getImagePath)
        self.select_sprite_btn.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def getImagePath(self):
        self.imgPath = filedialog.askopenfilename()
        return self.imgPath if len(self.imgPath) > 0 else "No image selected"

root = Tk()
my_gui = GUI(root)
root.mainloop()