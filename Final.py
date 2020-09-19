from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog   
from tkinter.filedialog import askopenfilename,  asksaveasfilename
from urllib.request import urlopen

import os
import cv2
import numpy
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from numpy import random, sqrt, log, sin, cos, pi
from scipy import ndimage

window = tk.Tk()
window.title('AIP Final')
window.geometry('1180x600')

# 創建打開圖像和顯示圖像函數
def Open_Img():
    global img_pnge, Img, file_path, img_gray, img, img_g
    OpenFile = tk.Tk() #創建新窗口
    OpenFile.withdraw()
    file_path = filedialog.askopenfilename()
    Img = Image.open(file_path)
    Img = Img.resize((550, 450), Image.ANTIALIAS)
    
    img_gray = Img.convert('L')
    img_pnge = ImageTk.PhotoImage(img_gray)
    label_Img = tk.Label(window, image=img_pnge)
    label_Img.place(x=20, y=80)
    plt.cla()
    img_array = np.array(img_gray)

    img = cv2.imread(file_path)
    img = cv2.resize(img,(550, 450))
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    plt.hist(img_array.ravel(), 256, [0, 256])
    plt.savefig('histogram.jpg')
   
def histogram():
    global img_png, Imgh
    
    Imgh = Image.open('histogram.jpg')
    Imgh = Imgh.resize((550, 450), Image.ANTIALIAS)

    img_png = ImageTk.PhotoImage(Imgh)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=600, y=80)

def gaussian():
    global height, width, G, sigma
    global img, img_g, f0, f1
    global gaussian, Gaussian
    
    img = cv2.imread(file_path)
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    f0 = img_g.copy()
    f1 = img_g.copy()   
    height, width = img_g.shape[:2]
    G=255   
    sigma = 0
    inputsigma()
    
def entersigma():
    global sigma
    sigma = int(entry.get())
    print(sigma)
    openwindow.destroy()
    step45()
 
def inputsigma():
    global openwindow, entry
    openwindow = tk.Tk()
    openwindow.title('Sigma')
    openwindow.geometry('300x100')
    
    entry = tk.Entry(openwindow)
    entry.place(x=50, y=0)
    entry.focus_set()    
    
    btn_Enter = tk.Button(openwindow,text="OK",command=entersigma)
    btn_Enter.place(x=130, y=50)
    
    openwindow.mainloop()

def step3():
    global phi, r, z1, z2
    phi = random.random()
    r = random.random()
    z1 = int(sigma * cos(2*pi*phi) * sqrt(-2*log(r)))
    z2 = int(sigma * sin(2*pi*phi) * sqrt(-2*log(r)))

def step45():
    for x in range (0, height, 2):
        for y in range (0, width):
            step3()     
            f0[x][y] = img_g[x][y]+z1
            f0[x+1][y] = img_g[x+1][y]+z2
            if f0[x][y] < 0:
                f1[x][y] = 0
            elif f0[x][y] > G-1 :
                f1[x][y] = G-1
            else :
                f1[x][y] = f0[x][y]
           
            if f0[x+1][y] < 0:
                f1[x+1][y] = 0
            elif f0[x+1][y] > G-1 :
                f1[x+1][y] = G-1
            else :
                f1[x+1][y] = f0[x+1][y]
                
    global gaus, Gaussian    
    cv2.imwrite('Gaussian.jpg', f1)
    gaus = Image.open('Gaussian.jpg')
    gaus = gaus.resize((550, 450), Image.ANTIALIAS)
    
    Gaussian = ImageTk.PhotoImage(gaus)
    label_Img = tk.Label(window, image=Gaussian)
    label_Img.place(x=20, y=80)

    plt.cla()
    img_array = np.array(gaus) 
    plt.hist(img_array.ravel(), 256, [0, 256])
    plt.savefig('histogram.jpg')

    
def enterlayer():
    global layer
    layer = int(entry.get())
    print(layer)
    openwindow.destroy()
    wavelet2() 
    
def inputlayer():
    global entry, buttom,openwindow
    openwindow = tk.Tk()
    openwindow.title('Layer')
    openwindow.geometry('300x100')
    
    entry = tk.Entry(openwindow)
    entry.place(x=50, y=0)
    entry.focus_set()
    btn_Enter = tk.Button(openwindow,text="OK",command=enterlayer)
    btn_Enter.place(x=130, y=50)
   
    openwindow.mainloop()
    
def haar(img):
    global image,height,width
    h = int(height/2)
    w = int(width/2)
    LL = np.zeros((h,w))
    LH = np.zeros((h,w))
    HH = np.zeros((h,w))
    HL = np.zeros((h,w))
    Lowpass = np.zeros((height,w))
    Highpass = np.zeros((height,w))
      
    for i in range (0,height):
        for j in range(0,width,2):
            w1 = int(j/2)
            Lowpass[i,w1] = int((img[i,j]/2) + (img[i,j+1]/2))
            Highpass[i,w1] = img[i,j] - Lowpass[i,w1] 
    
    p,q = Lowpass.shape        
    for i in range (0,p,2):
        for j in range(0,q):
            h1 = int(i/2)
            LL[h1,j] = int((Lowpass[i,j]/2) + (Lowpass[i+1,j]/2))
            LH[h1,j] = int((Lowpass[i,j]) - LL[h1,j])
            HH[h1,j] = int((Highpass[i,j]/2) + Highpass[i,j]/2)
            HL[h1,j] = int(Highpass[i,j] - HL[h1,j])
  
    LH[LH < 0] = 0
    LH = cv2.normalize(LH,None,0,255,cv2.NORM_MINMAX)
    HL[HL < 0] = 0
    HL = cv2.normalize(HL,None,0,255,cv2.NORM_MINMAX)
    HH[HH < 0] = 0
    HH = cv2.normalize(HH,None,0,255,cv2.NORM_MINMAX)    

    image[0:h,0:w] = LL[:,:]
    image[h:height,0:w] = HL[:,:]
    image[0:h,w:width] = LH[:,:]
    image[h:height,w:width] = HH[:,:]

    height = int(height/2)
    width = int(width/2)
        
def wavelet():
    global image,height,width,imgg
    imgg = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    height,width = imgg.shape
    image = np.zeros((height,width))
    inputlayer()


def wavelet2():
    global image,imgg,layer
    for i in range(0,layer):
        if i == 0:
            haar(imgg)
        else :
            haar(image)
            
    cv2.imwrite('DWT.jpg', image)
    show()
    
def show():
    global img_png, Imgh
    Imgh = Image.open('DWT.jpg')
    Imgh = Imgh.resize((550, 450), Image.ANTIALIAS)

    img_png = ImageTk.PhotoImage(Imgh)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=600, y=80)


def equalization():
    global img_gray, img_g, AB
    #直方圖
    pixels = img_gray.load()
    width, height = img_gray.size
    total = width * height
    all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            all_pixels.append(cpixel)
    H = []
    for i in range (0, 256):
        H.append(all_pixels.count(i))

    all_count = H.copy()
    for number in range (0,256):
                mid = max(all_count) - min(all_count)
                all_count[number] = (all_count[number] - min(all_count)) / mid *int(max(all_count))
    im = Image.new("RGB", (514, int(max(all_count)+50)), color="white")
    draw = ImageDraw.Draw(im)
 
    for t in range (0,256):
        draw.line((t*2, 0, t*2, all_count[t]), fill = 'black', width=2)    
     
    im_t = im.transpose(Image.FLIP_TOP_BOTTOM)
    print(H)
    
    #均衡化 
    gmin = min(H)
    Hc = H.copy()
    T = np.zeros(256)
    for i in range (1,256):
        Hc[i] = Hc[i-1]+H[i]
    Hmin = Hc[gmin]
    for i in range(256):
        T[i] = int(((Hc[i]-Hmin)/(Hc[255]-Hmin))*(255))

    Himg = img_g.copy()
    n,m = img_g.shape
    for i in range(n):
        for j in range(m):
            temp = img_g[i][j]
            Himg[i][j] = T[temp]
            
    Himg_pixels = []
    for x in range(n):
        for y in range(m):
            cpixel = Himg[x][y]
            Himg_pixels.append(cpixel)

    cv2.imwrite('his.jpg', Himg)
    
    Himg_count = []
    for i in range (0, 256):
        print('running')
        Himg_count.append(Himg_pixels.count(i))
    for number in range (0,256):
                mid = max(Himg_count) - min(Himg_count)
                Himg_count[number] = (Himg_count[number] - min(Himg_count)) / mid *int(max(Himg_count))

    AB = Image.new("RGB", (514, int(max(Himg_count)+50)), color="white")
    drawAB = ImageDraw.Draw(AB)
    
    for t in range (0,256):
        drawAB.line((t*2, 0, t*2, Himg_count[t]), fill = 'black', width=2)    
    
    AB = AB.transpose(Image.FLIP_TOP_BOTTOM)
    AB = AB.resize((550, 450), Image.ANTIALIAS)
   
    print(Himg_count)
    show2()

def show2():
    global img_png, Imgh ,img_AB, AB
    
    Imgh = Image.open('his.jpg')
    Imgh = Imgh.resize((550, 450), Image.ANTIALIAS)

    img_png = ImageTk.PhotoImage(Imgh)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=20, y=80)
    

    img_AB = ImageTk.PhotoImage(AB)
    label_Img = tk.Label(window, image=img_AB)
    label_Img.place(x=600, y=80)


        
def masksize():
    global Size
    Size = int(entry.get())
    print(Size)
    openwindow.destroy()
    Smoothing()   
    
def Convolution():
    global entry, buttom,openwindow
    openwindow = tk.Tk()
    openwindow.title('Mask Size')
    openwindow.geometry('300x100')
    
    entry = tk.Entry(openwindow)
    entry.place(x=50, y=0)
    entry.focus_set()
    btn_Enter = tk.Button(openwindow,text="OK",command = masksize)
    btn_Enter.place(x=130, y=50)
    
    openwindow.mainloop()


def Smoothing():
    global Size, img, my_conImg,conImg,conImgf
    num = Size
    conImg =img_g.copy()
    h,w = conImg.shape
    kernel = num*num
    space = int((num-1)/2) 
    
    a = np.pad(conImg, int(num/2), mode='constant')
    ah,aw = a.shape
    for i in range(0, ah-num+1):
        for j in range(0, aw-num+1):
            conImg[i][j] = int((np.sum(a[i : i+num , j : j+num]))/kernel)

    cv2.imwrite('Smoothing.jpg', conImg)
    show_s()

def show_s():
    global img_png, Imgh
    
    Imgh = Image.open('Smoothing.jpg')
    Imgh = Imgh.resize((550, 450), Image.ANTIALIAS)

    img_png = ImageTk.PhotoImage(Imgh)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=20, y=80)



def hysteresis(img, weak, strong=255):
    global hys
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong) or (img[i-1, j-1] == strong)
                        or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)): img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    hys = img            
    cv2.imwrite('hysteresis.jpg',img)
    show_h()
 
#edge linking
def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
    global res
    highThreshold = img.max() * highThresholdRatio;
    lowThreshold = highThreshold * lowThresholdRatio;
    
    M, N = img.shape
    res = np.zeros((M,N), dtype=np.int32)
    
    weak = np.int32(25)
    strong = np.int32(255)
    
    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)   
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    
    cv2.imwrite('threshold.jpg',res)
    hysteresis(res, 75, 100)

#non_max_suppression
def non_max_suppression(img, D):
    global Z
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j]
                else:
                    Z[i,j] = 0
            except IndexError as e:
                pass   


    cv2.imwrite('non_max_sup.jpg',Z)
    threshold(Z)

def Canny():
    sobelr = np.array([[-1, 0, 1]], np.float32) #行/列
    sobelc = np.array([[1, 2, 1]], np.float32) #行/列
    
    Fx0 = np.zeros(shape = (conImg.shape[0],conImg.shape[1]-2))     
    Fx = np.zeros(shape = (Fx0.shape[0]-2,Fx0.shape[1]))     
    Fy0 = np.zeros(shape = (conImg.shape[0],conImg.shape[1]-2))     
    Fy = np.zeros(shape = (Fy0.shape[0]-2,Fx0.shape[1]))   
    cv2.imwrite('conImg.jpg', conImg)    

    for x in range(0, (conImg.shape[0])):  #高0-99共100
        for y in range(0, (conImg.shape[1]-2)): #行  
            Fx0[x,y] = np.multiply(conImg[x, y: y + 3], sobelr).sum()/8
            
    for x in range(0, (Fx0.shape[0]-2)):  #高
        for y in range(0, (Fx0.shape[1])): #行 
            Fx[x,y] = np.multiply(Fx0[x:x+3,y], sobelc).sum()/8
    
    for x in range(0, (conImg.shape[0])):  #高0-99共100
        for y in range(0, (conImg.shape[1]-2)): #行  
            Fy0[x,y] = np.multiply(conImg[x, y: y + 3], sobelc).sum()/8
            
    for x in range(0, (Fy0.shape[0]-2)):  #高
        for y in range(0, (Fy0.shape[1])): #行 
            Fy[x,y] = np.multiply(Fy0[x:x+3,y], sobelr).sum()/8
            
    sobel = np.sqrt(np.add(np.square(Fx), np.square(Fy)))
    sobel = sobel / sobel.max()*255
    theta = np.arctan2(Fx, Fy)     
    cv2.imwrite('sobel.jpg', sobel)    
    non_max_suppression(sobel, theta)

def show_h():


    global img_png, Imgh, Imghh ,img_hys, hys
    
    Imgh = Image.open('Smoothing.jpg')
    Imgh = Imgh.resize((550, 450), Image.ANTIALIAS)

    img_png = ImageTk.PhotoImage(Imgh)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=20, y=80)

    Imghh = Image.open('hysteresis.jpg')
    Imghh = Imghh.resize((550, 450), Image.ANTIALIAS)
    
    img_hys = ImageTk.PhotoImage(Imghh)
    label_Img = tk.Label(window, image=img_hys)
    label_Img.place(x=600, y=80)




def save():
    filename = filedialog.asksaveasfilename(initialdir = "C:/Users/Vivian Hu/Desktop/"
                                 ,title = "Select file",filetypes =
                                 ([("PNG", "*.png"),("JPEG", "*.jpg"),
                                   ("BMP", "*.BMP"),("PPM", "*.ppm"),
                                   ("All files", "*")]), defaultextension = "*.*")
    Imgh.save(filename)
    

# 創建打開圖像按鈕
btn_Open = tk.Button(window,text='檔案', width=10, height=2, command=Open_Img)
btn_Open.place(x=10,y=20)
btn_Save = tk.Button(window, text = "直方圖", width=10, height=2, command = histogram )
btn_Save.place(x=120,y=20)
btn_Gaussian = tk.Button(window, text = "高斯雜訊", width=10, height=2, command = gaussian )
btn_Gaussian.place(x=230,y=20)
btn_wavelets = tk.Button(window,text = "小波", width=10, height=2, command = wavelet)
btn_wavelets.place(x=340,y=20)
btn_wavelets = tk.Button(window,text = "直方圖均化", width=10, height=2, command = equalization)
btn_wavelets.place(x=450,y=20)
btn_wavelets = tk.Button(window,text = "平滑化", width=10, height=2, command = Convolution)
btn_wavelets.place(x=560,y=20)
btn_wavelets = tk.Button(window,text = "邊緣偵測", width=10, height=2, command = Canny)
btn_wavelets.place(x=670,y=20)
btn_Save = tk.Button(window, text = "儲存", width=10, height=2, command = save )
btn_Save.place(x=780,y=20) 

window.mainloop()
