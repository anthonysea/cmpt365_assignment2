from tkinter import *
import tkinter.filedialog as filedialog
import PIL
from PIL import Image, ImageTk
import cv2
import numpy as np

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

        # quantization values from textbook
        QY = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                       [12, 12, 14, 19, 26, 48, 60, 55],
                       [14, 13, 16, 24, 40, 57, 69, 56],
                       [14, 17, 22, 29, 51, 87, 80, 62],
                       [18, 22, 37, 56, 68, 109, 103, 77],
                       [24, 35, 55, 64, 81, 104, 113, 92],
                       [49, 64, 78, 87, 103, 121, 120, 101],
                       [72, 92, 95, 98, 112, 100, 103, 99]])

        QC = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                       [18, 21, 26, 66, 99, 99, 99, 99],
                       [24, 26, 56, 99, 99, 99, 99, 99],
                       [47, 66, 99, 99, 99, 99, 99, 99],
                       [99, 99, 99, 99, 99, 99, 99, 99],
                       [99, 99, 99, 99, 99, 99, 99, 99],
                       [99, 99, 99, 99, 99, 99, 99, 99],
                       [99, 99, 99, 99, 99, 99, 99, 99]])

        self.Q = [QY, QC, QC]


    def displayImage(self, identifier):
        self.imgPath = filedialog.askopenfilename()
        if identifier == "scene":
            self.sceneImg = Image.open(self.imgPath)
            self.scenePhoto = ImageTk.PhotoImage(self.sceneImg)
            self.sceneLabel.config(image=self.scenePhoto)
            self.sceneLabel.pack(side="left")

        else:
            self.spriteImg = Image.open(self.imgPath)
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
        self.h, self.w = self.mergedImgRaw.shape[:2]



        # dct transform

        transformVals = []
        imgQuantVals = []
        blockSize = 8

        for idx, channel in enumerate(self.imgSub):
            # width and height of channel
            chanRows = channel.shape[0]
            chanCols = channel.shape[1]

            # zero the matrices
            transformBlock = np.zeros((chanRows, chanCols), np.float32)
            transformQuant = np.zeros((chanRows, chanCols), np.float32)

            # set block width and height
            blockHeight = chanRows / blockSize
            blockWidth = chanCols / blockSize

            # create a copy of the img and zero it's matrix
            vis0 = np.zeros((chanRows, chanCols), np.float32)
            vis0[:chanRows, :chanCols] = channel
            vis0 -= 128 # offset the vals by 128
            for row in range(int(blockHeight)):
                for col in range(int(blockWidth)):
                    currentBlock = cv2.dct(vis0[row * blockSize: (row + 1) * blockSize, col * blockSize: (col + 1) * blockSize])
                    transformBlock[row * blockSize: (row + 1) * blockSize, col * blockSize: (col + 1) * blockSize] = currentBlock
                    transformQuant[row * blockSize: (row + 1) * blockSize, col * blockSize: (col + 1) * blockSize] = np.round(currentBlock / self.Q[idx])
            transformVals.append(transformBlock)
            imgQuantVals.append(transformQuant)

        np.save('compressed.mrg', imgQuantVals)
        print(imgQuantVals)

        # flatten array
        for channel in range(len(imgQuantVals)):
            imgQuantVals[channel] = imgQuantVals.flatten()

        flattened = np.append(imgQuantVals[0], [imgQuantVals[1], imgQuantVals[2], [self.h, self.w]])
        np.savetxt('compressed.mrg', flattened)


root = Tk()
app = App(root)
root.mainloop()