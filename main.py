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
                                       padx="2", pady="2").grid(row=0, column=0, sticky="WE", pady="5")

        self.select_sprite_btn = Button(frame, text="Select sprite", command=lambda: self.displayImage("sprite"),
                                        padx="2", pady="2").grid(row=0, column=1, sticky="WE", pady="5")

        self.merge_btn = Button(frame, text="Merge", padx="2", pady="2",
                                command=self.mergeImages).grid(row=0, column=2, sticky="WE", pady="5")


        self.compress_save_btn = Button(frame, text="Save & compress",
                               padx="2", pady="2", command=self.compress).grid(row=0, column=3, sticky="WE", pady="5")


        self.close_button = Button(frame, text="Close", command=frame.quit,
                                   padx="2", pady="2").grid(row=0, column=4, sticky="WE", pady="5")


        self.sceneLabel = Label(root)
        self.spriteLabel = Label(root)
        self.mergedLabel = Label(root)


    def displayImage(self, identifier):
        self.imgPath = filedialog.askopenfilename()
        if identifier == "scene":
            self.sceneImg = Image.open(self.imgPath)
            # self.sceneImg.thumbnail((256,256))
            '''
            self.scenePhoto = ImageTk.PhotoImage(self.sceneImg)
            self.sceneCanvas.create_image((0, 0), image=self.scenePhoto, anchor="nw")
            self.sceneCanvas.image = self.scenePhoto
            self.sceneCanvas.pack()
            '''
            self.scenePhoto = ImageTk.PhotoImage(self.sceneImg)
            self.sceneLabel.config(image=self.scenePhoto)
            self.sceneLabel.pack(side="left")

        else:
            self.spriteImg = Image.open(self.imgPath)
            # self.spriteImg.thumbnail((256,256))
            '''
            self.spritePhoto = ImageTk.PhotoImage(Image.open(self.imgPath))
            self.spriteCanvas.create_image((0, 0), image=self.spritePhoto, anchor="nw")
            self.spriteCanvas.image = self.spritePhoto
            self.spriteCanvas.pack()
            '''
            self.spritePhoto = ImageTk.PhotoImage(self.spriteImg)
            self.spriteLabel.config(image=self.spritePhoto)
            self.spriteLabel.pack(side="left")


    def mergeImages(self):
        self.mergedImg = self.sceneImg
        spriteWidth, spriteHeight = self.spriteImg.size
        sceneWidth, sceneHeight = self.sceneImg.size
        offset = (int((sceneWidth - spriteWidth) / 2), int((sceneHeight - spriteHeight) / 2))
        # need to figure out way to build a proper mask, greyscale mask doesn't work correctly
        mask = self.spriteImg.convert("1")
        self.mergedImg.paste(self.spriteImg, offset, mask)
        self.mergedImg.save('merged.png')
        self.mergedImg.show()
        #self.mergedPhoto = ImageTk.PhotoImage(self.mergedImg)
        #self.mergedLabel.config(image=self.mergedPhoto)
        #self.mergedLabel.pack(side="left")

    def compress(self):
        # convert image from RGB to YUV
        self.mergedImgRaw = cv2.imread('merged.png')
        self.mergedImgRaw = cv2.cvtColor(self.mergedImgRaw, cv2.COLOR_BGR2YUV)

        subsampleV = 4
        subsampleH = 4
        uf = cv2.boxFilter(self.mergedImgRaw[:,:,1], ddepth=-1, ksize=(2,2))
        vf = cv2.boxFilter(self.mergedImgRaw[:,:,2], ddepth=-1, ksize=(2,2))
        u_sub = uf[::subsampleV, ::subsampleH]
        v_sub = vf[::subsampleV, ::subsampleH]
        self.imgSub = [self.mergedImgRaw[:,:,0], u_sub, v_sub]

        npArray = numpy.asarray(self.imgSub)
        testImg = Image.fromarray(npArray, mode="YCbCr")
        testImg.show()




root = Tk()
#root.resizable(width=True, height=True)
app = App(root)
root.mainloop()