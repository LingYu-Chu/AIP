from PIL import Image, ImageTk # 導入圖像處理函數庫
from matplotlib import pyplot as plt
import tkinter as tk           # 介面
import tkinter.filedialog
import os.path
import numpy as np

# 設定窗口大小命名
window = tk.Tk()
window.title('AIP 60847017S')
window.geometry('1200x600')
global img, img_png, show_dwt, level

#輸入層數
level_input = tk.Label(window, text = "輸入層數：")
level_input.place(x = 400, y = 22)
level_text = 'a'
level_text = tk.Entry(window, show = None, width = 5) #輸入框
level_text.place(x = 480, y = 20)

# 打開圖像 顯示圖像
def Open_Img():
    global img, img_png
    filename = tkinter.filedialog.askopenfilename(filetypes = [("Image files",("*.jpg","*.jpeg","*.ppm","*.bmp"))])
    img_name = os.path.basename(filename)
    img_open = Image.open(filename)
    img_show = img_open.resize( (512, 512), Image.BILINEAR ) #將影像轉成512x512
    img = np.array(img_show)

    img_show2 = img_open.resize( (400, 400), Image.BILINEAR ) #顯示圖像的大小
    img_show2 = img_show2.convert('L')
    img_png = ImageTk.PhotoImage(img_show2)
    label_Img = tk.Label(window, image = img_png)
    label_Img.place(x = 100, y = 100) # 第一張圖的位置
    rows, cols, dims = img.shape 
    R = np.mat(img[:, :, 0])
    G = np.mat(img[:, :, 1])
    B = np.mat(img[:, :, 2])
    img = R * 0.299 + G * 0.587 + B * 0.114

# Daubechies Scaling/Wavelet (low/high pass) filter
DB={
    # Haar
    'L1':[ 0.7071067811865476,0.7071067811865476],
    'H1':[-0.7071067811865476,0.7071067811865476],
    # Daubechies2 Low/High pass (Scaling/Wavelet filter)
    'L2':[-0.1294095226,0.2241438680, 0.8365163037, 0.4829629131], # scaling filter
    'H2':[-0.4829629131,0.8365163037,-0.2241438680,-0.1294095226], # wavelet filter
    # Daubechies3 Low/High pass filter
    'L3':[0.0352262919,-0.0854412739,-0.1350110200,\
          0.4598775021,0.8068915093,0.3326705530],
    'H3':[-0.3326705530,0.8068915093,-0.4598775021,\
          -0.1350110200,0.0854412739,0.0352262919],
    # Daubechies4 Low/High pass filter
    'L4':[-0.0105974018,0.0328830117,0.0308413818,-0.1870348117,\
          -0.0279837694,0.6308807679,0.7148465706, 0.2303778133],
    'H4':[-0.2303778133,0.7148465706,-0.6308807679,-0.0279837694,\
          0.1870348117,0.0308413818,-0.0328830117,-0.0105974018],
    # Daubechies5 Low/High pass filter
    'L5':[0.0033357253,-0.0125807520,-0.0062414902,0.0775714938,-0.0322448696,\
         -0.2422948871, 0.1384281459, 0.7243085284,0.6038292698, 0.1601023980],
    'H5':[-0.1601023980, 0.6038292698,-0.7243085284,0.1384281459,0.2422948871,\
          -0.0322448696,-0.0775714938,-0.0062414902,0.0125807520,0.0033357253],
    # Daubechies6 Low/High pass filter
    'L6':[-0.0010773011, 0.0047772575, 0.0005538422,-0.0315820393,\
           0.0275228655, 0.0975016056,-0.1297668676,-0.2262646940,\
           0.3152503517, 0.7511339080, 0.4946238904,0.1115407434],
    'H6':[-0.1115407434, 0.4946238904,-0.7511339080,0.3152503517,\
           0.2262646940,-0.1297668676,-0.0975016056,0.0275228655,\
           0.0315820393,0.0005538422,-0.0047772575,-0.0010773011]
}

# Daubechies coefficients
firDec=(DB['L1'],DB['H1']) #使用haar 作為mother wavelets

# DWT decomposition and sub sampling
def dwt_decomposition_x(inImage,firset):
    L,H=firset
    L=np.array(L).astype('float64') #numpy數組 dtype為float64
    H=np.array(H).astype('float64')
    n=int(len(L)) # tap=n/2: vanishing moment
    t=n-1 # offset
    rows,cols=inImage.shape #512,512
    hsize=int(cols/2) #切一半
    data=np.zeros((rows,cols),dtype=np.float64)
    data[:,:]=inImage[:,:]
    dwt=np.zeros((rows,cols),dtype=np.float64)
    for row in range(0,rows): # low pass
        for col in range(0,hsize):
            for i in range(0,n):
                dwt[row,col]+=data[row,((col<<1)-t+i)%cols]*L[i]
    for row in range(0,rows): # high pass
        for col in range(0,hsize):
            for i in range(0,n):
                dwt[row,col+hsize]+=data[row,((col<<1)-t+i)%cols]*H[i]
    return dwt

def dwt_decomposition_y(inImage,firset):
    L,H=firset
    L=np.array(L).astype('float64')
    H=np.array(H).astype('float64')
    n=int(len(L)) # tap=n/2: vanishing moment
    t=n-1 # offset
    rows,cols=inImage.shape
    hsize=int(cols/2)
    data=np.zeros((rows,cols),dtype=np.float64)
    data[:,:]=inImage[:,:]
    dwt=np.zeros((rows,cols),dtype=np.float64)
    for row in range(0,hsize): # low pass
        for col in range(0,cols):
            for i in range(0,n):
                dwt[row,col]+=data[((row<<1)-t+i)%rows,col]*L[i]
    for row in range(0,hsize): # high pass
        for col in range(0,cols):
            for i in range(0,n):
                dwt[row+hsize,col]+=data[((row<<1)-t+i)%rows,col]*H[i]
    return dwt

# DWT 2D
def dwt_2d(img,firSet,level):
    rows,cols=img.shape
    data=np.zeros((rows,cols))
    data[:,:]=img[:,:]
    while level>0:
        buf=data[:rows,:cols]
        dwt=dwt_decomposition_x(buf,firDec)
        dwt=dwt_decomposition_y(dwt,firDec)
        data[:rows,:cols]=dwt[:rows,:cols]
        level-=1
        rows>>=1
        cols>>=1
    return data

def transform():
    global show_dwt, level, img
    level = level_text.get() #抓取輸入的層數
    level = int(level)
    rows,cols=img.shape
    csize=cols>>level

    # DWT decomposition
    dwt=dwt_2d(img,firDec,level)

    # visualization
    tmp=np.zeros((rows,cols))
    tmp[:,:]=255-dwt[:,:]*10
    tmp[:csize,:csize]=0.5/level*dwt[:csize,:csize]

    plt.imshow(tmp,vmin=0,vmax=255)
    plt.savefig('dwt.png')
    dwt_img = Image.open('dwt.png')
    dwt_img = dwt_img.convert('L')

    show_dwt= ImageTk.PhotoImage(dwt_img)
    label_Img2= tk.Label(window, image = show_dwt)
    label_Img2.place(x = 540, y = 50) #第二張圖的位置

# 創建打開影像按鈕 
btn_Open = tk.Button(window,
    text = '選擇圖像',      
    width = 13, height = 2,
    command = Open_Img)     # 執行open img
btn_Open.place(x = 100, y = 20)    # 按鈕位置

# 創建小波轉換按鈕
btn_Open = tk.Button(window,
    text = '小波轉換',      
    width = 13, height = 2,
    command = transform)     # 執行open img
btn_Open.place(x = 250, y = 20)    # 按鈕位置

# 運行整體窗口
window.mainloop()