#創建GUI窗口打開圖像 顯示在窗口中
from PIL import Image, ImageTk # 導入圖像處理函數庫
import matplotlib.pyplot as plt # 繪圖庫
import numpy as np
import tkinter as tk           # 介面
import tkinter.filedialog
import os.path

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
    img2 = img.convert('L') # 轉成灰階 L- 8位像素，黑白

    ratio = float(width)/img2.size[0] # 寬300 
    height = int(img.size[1]*ratio) # 以原始比率調整整張大小 
    nim = img2.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片

    img_png = ImageTk.PhotoImage(nim)
    label_Img = tk.Label(window, image = img_png)
    label_Img.place(x = 100, y = 120) # 第一張圖的位置

    var.set('所選影像：' + str(img_name) + '  |  影像大小：' + str(img.size) + ' → ' + str(nim.size))

# 處理影像灰階直方圖
def Image_histogram():
    plt.cla() # Clear axis
    global nim, show_hist
    n_nim = np.array(nim) # 轉成array
    arr = n_nim.flatten() # 降到一維
    hist = plt.hist(arr, bins = 256, density = 1, facecolor = 'cadetblue', alpha = 0.75) # arr計算一維數組、bin:圖的柱數、normed:向量歸一化
    plt.savefig('hist.png')
    hist_img = Image.open('hist.png')

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

Label_Show = tk.Label(window,
    textvariable = var,   # 使用 textvariable 替換 text, 文字可以做變化
    width = 70, height = 2)
Label_Show.place(x = 100, y = 70)

# 運行整體窗口
window.mainloop()