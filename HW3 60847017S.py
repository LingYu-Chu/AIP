#創建GUI窗口打開圖像 顯示在窗口中
#encoding: utf-8

from PIL import Image, ImageTk # 導入圖像處理函數庫
import matplotlib.pyplot as plt # 繪圖庫
import numpy as np
import tkinter as tk           # 介面
import tkinter.filedialog
import os.path
import math
import random
import cv2
import scipy.misc
import scipy.signal
import scipy.ndimage
from math import sqrt, log, cos, sin, pi

# 設定窗口大小命名
window = tk.Tk()
window.title('AIP 60847017S')
window.geometry('850x500')
global img_png, image, nim, show_hist            # 定義img_png
var = tk.StringVar()    
width = 300

# 打開圖像 顯示圖像
def Open_Img():
    global img_png, nim, img_name
    filename = tkinter.filedialog.askopenfilename(filetypes = [("Image files",("*.jpg","*.jpeg","*.ppm","*.bmp"))])
    img_name = os.path.basename(filename)
    print('檔名：' + os.path.basename(filename))
    img = Image.open(filename)
    #img2 = img.convert('L') # 轉成灰階 L- 8位像素，黑白

    ratio = float(width)/img.size[0] # 寬300 
    height = int(img.size[1]*ratio) # 以原始比率調整整張大小 
    nim = img.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片

    img_png = ImageTk.PhotoImage(nim)
    label_Img = tk.Label(window, image = img_png)
    label_Img.place(x = 100, y = 120) # 第一張圖的位置

    var.set('所選影像：' + str(img_name) + '  |  影像大小：' + str(img.size) + ' → ' + str(nim.size))

# 高斯雜訊
def add_gaussian_noise():
    global nim
    #nim = nim..convert('L')
    nim = np.array(nim)
    #plt.cla() # Clear axis
    rows, cols, dims = nim.shape 
    R = np.mat(nim[:, :, 0])
    G = np.mat(nim[:, :, 1])
    B = np.mat(nim[:, :, 2])
    Grey_gs = R * 0.299 + G * 0.587 + B * 0.114

    snr = 0.9
    mean = 0
    sigma = 30
    percetage = 0.8
    r = random.random() #in the range[0,1]
    v = random.random()
    print('hi,in')
    NoiseImg = Grey_gs
    NoiseNum = int(percetage*nim.shape[0]*nim.shape[1])
    for i in range(NoiseNum):
        randX=random.randint(0,nim.shape[0]-1)
        randY=random.randint(0,nim.shape[1]-1)
        z1 = sqrt(-2 * log(r)) * cos(2 * pi * v) * sigma #step3
        z2 = sqrt(-2 * log(r)) * sin(2 * pi * v) * sigma
        NoiseImg[randX, randY]=NoiseImg[randX,randY]+ z1 #step4
        NoiseImg[randX, randY]=NoiseImg[randX,randY]+ z2
        if  NoiseImg[randX, randY]< 0:
            NoiseImg[randX, randY]=0
        elif NoiseImg[randX, randY]>255:
            NoiseImg[randX, randY]=255

    NoiseImg=NoiseImg.astype(np.uint8)
    plt.savefig('noise.png',cmap='gray')
    print('saved')
    noise_img = Image.open('Figure_1.png')
    ratio = float(400) / noise_img.size[0] # 寬300 
    height = int(noise_img.size[1]*ratio) # 以原始比率調整整張大小 
    n_noise_im = noise_img.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片

    show_noise= ImageTk.PhotoImage(n_noise_im)
    label_Img2= tk.Label(window, image = show_noise)
    label_Img2.place(x = 450, y = 120) #第二張圖的位置
    plt.title('Grey gauss noise')
    plt.imshow(NoiseImg, cmap='gray')
    plt.show()
    

# 處理影像灰階直方圖
def Image_histogram():
    plt.cla() # Clear axis
    global nim, show_hist
    n_nim = np.array(nim) # 轉成array
    arr = n_nim.flatten() # 降到一維
    hist = plt.hist(arr, bins = 256, density = 1, facecolor = 'cadetblue', alpha = 0.75) # arr計算一維數組、bin:圖的柱數、normed:向量歸一化
    plt.savefig('hist.jpg')
    hist_img = Image.open('hist.jpg')

    ratio = float(400) / hist_img.size[0] # 寬300 
    height = int(hist_img.size[1]*ratio) # 以原始比率調整整張大小 
    n_hist_im = hist_img.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片

    show_hist= ImageTk.PhotoImage(n_hist_im)
    label_Img3= tk.Label(window, image = show_hist)
    label_Img3.place(x = 450, y = 100) #第二張圖的位置


# 創建打開影像按鈕 
btn_Open = tk.Button(window,
    text = '選擇圖像',      
    width = 13, height = 2,
    command = Open_Img)     # 執行open img
btn_Open.place(x = 100, y = 20)    # 按鈕位置

# 創建灰階直方圖按鈕
btn_Open = tk.Button(window,
    text = '直方圖',      
    width = 13, height = 2,
    command = Image_histogram)     # 執行open img
btn_Open.place(x = 250, y = 20)    # 按鈕位置

# 高斯雜訊
btn_Open = tk.Button(window,
    text = '高斯雜訊',      
    width = 13, height = 2,
    command = add_gaussian_noise)     # 執行open img
btn_Open.place(x = 400, y = 20)    # 按鈕位置

Label_Show = tk.Label(window,
    textvariable = var,   # 使用 textvariable 替換 text, 文字可以做變化
    width = 70, height = 2)
Label_Show.place(x = 100, y = 70)

# 運行整體窗口
window.mainloop()