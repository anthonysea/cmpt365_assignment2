from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np


# block size for chunks
blockSize = 8
# quantization arrays from textbook
QY=np.array([[16,11,10,16,24,40,51,61],
             [12,12,14,19,26,48,60,55],
             [14,13,16,24,40,57,69,56],
             [14,17,22,29,51,87,80,62],
             [18,22,37,56,68,109,103,77],
             [24,35,55,64,81,104,113,92],
             [49,64,78,87,103,121,120,101],
             [72,92,95,98,112,100,103,99]])

QC=np.array([[17,18,24,47,99,99,99,99],
             [18,21,26,66,99,99,99,99],
             [24,26,56,99,99,99,99,99],
             [47,66,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99],
             [99,99,99,99,99,99,99,99]])

Q = [QY, QC, QC]

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.load_img_btn = Button(frame, text="Select file", command=lambda: self.loadImage(),
                                   padx="2", pady="2")
        self.load_img_btn.pack()

    def loadImage(self):
        # load file to decompress
        imgPath = filedialog.askopenfilename()
        print(imgPath)
        self.decompress(imgPath)


    def decompress(self, imgPath):
        # load quantization array
        imgQuantVals = np.load('compressed.mrg.npy')

        h = len(imgQuantVals[0])
        w = len(imgQuantVals[0][0])
        print(h, w)

        DecAll = np.zeros((int(h), int(w), 3), np.uint8)

        # run idct transform on each block
        for id, channel in enumerate(imgQuantVals):
            chanRows = channel.shape[0]
            chanCols = channel.shape[1]
            blocksV = chanRows / blockSize
            blocksH = chanCols / blockSize
            back0 = np.zeros((chanRows, chanCols), np.uint8)
            for row in range(int(blocksV)):
                for col in range(int(blocksH)):
                    dequantBlock = channel[row * blockSize: (row + 1) * blockSize, col * blockSize: (col + 1) * blockSize] * Q[id]
                    currentBlock = np.round(cv2.idct(dequantBlock)) + 128
                    currentBlock[currentBlock > 255] = 255
                    currentBlock[currentBlock < 0] = 0
                    back0[row * blockSize: (row + 1) * blockSize, col * blockSize: (col + 1) * blockSize] = currentBlock
            back0 = cv2.resize(back0, (int(w), int(h)))
            DecAll[:, :, id] = np.round(back0)

        restoredImg = cv2.cvtColor(DecAll, cv2.COLOR_YUV2BGR)
        cv2.imshow('', restoredImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def flatten():
    # flatten 


root = Tk()
#root.resizable(width=True, height=True)
app = App(root)
root.mainloop()