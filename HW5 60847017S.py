#創建GUI窗口打開圖像 顯示在窗口中
from PIL import Image, ImageTk, ImageDraw # 導入圖像處理函數庫
import matplotlib.pyplot as plt # 繪圖庫
import numpy as np
import tkinter as tk           # 介面
import tkinter.filedialog
import os.path

# 設定窗口大小命名
window = tk.Tk()
window.title('AIP 60847017S')
window.geometry('1000x800')
global img_png, image, nim, show_hist            # 定義img_png
var = tk.StringVar()    
width = 300

# 打開圖像 顯示圖像
def Open_Img():
    global img_png, nim, img_name, img2
    filename = tkinter.filedialog.askopenfilename(filetypes = [("Image files",("*.jpg","*.jpeg","*.ppm","*.bmp"))])
    img_name = os.path.basename(filename)
    img = Image.open(filename)
    img2 = img.convert('L') # 轉成灰階 L- 8位像素，黑白

    ratio = float(width)/img2.size[0] # 寬300 
    height = int(img.size[1]*ratio) # 以原始比率調整整張大小 
    nim = img2.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片

    img_png = ImageTk.PhotoImage(nim)
    label_Img = tk.Label(window, image = img_png)
    label_Img.place(x = 100, y = 80) # 第一張圖的位置

# 處理影像灰階直方圖
def Image_histogram():
    global img2, show_his
    #計算每個像素值的總和
    image_sum = [0] * 256
    image_pix = img2.load()

    for i in range(img2.size[0]):
        for j in range(img2.size[1]):
            image_sum[image_pix[i, j]] = image_sum[image_pix[i, j]] + 1

    for i in range(len(image_sum)):
        image_sum[i] = round((image_sum[i] - min(image_sum))* 600 / max(image_sum) - min(image_sum)) #size=600
    image_sum_new = image_sum

    his = Image.new("L", (512 , 700), 255) #("mode",size) L:灰階
    draw = ImageDraw.Draw(his)
    for i in range(256):
        if(image_sum_new[i]>0):
            draw.line([(i*2,645),(i*2,645-image_sum_new[i])],fill=100,width=2) #xy座標列表, fill=線條顏色, width=線條寬度
        draw.rectangle([(i*2,650),(i*2+2,700)],fill=i)
    
    his = his.resize( (255, 350), Image.BILINEAR )
    show_his = ImageTk.PhotoImage(his)
    label_Img2 = tk.Label(window, image = show_his)
    label_Img2.place(x = 120, y = 400) # 第二張圖的位置
    

def histogram_equalization():
    global img2, show_hist_equal_img, show_equal_his
    MN = img2.size[0]*img2.size[1]
    M = img2.size[0]
    N = img2.size[1]
    print(M)
    print(N)
    t = [0] * 256
    t = np.array(t, dtype=np.uint8)
    image_count = [0] * 256
    image_arr = img2.load()
    for i in range(img2.size[0]):
        for j in range(img2.size[1]):
            image_count[image_arr[i, j]] = image_count[image_arr[i, j]] + 1
    #image_count = np.array(image_count)
    g_min = (np.array(image_count) != 0).argmax(axis = 0) #找到array中第一個非0的值
    print("gmin:"+str(g_min))
    image_cumsum_count = np.cumsum(image_count) #直接用.cumsum算累加求和
    min_count = image_cumsum_count[g_min]
    for i in range(0 , 256):
        ratio = (image_cumsum_count[i] - min_count)/(MN - min_count) #第四步驟Hc[g]-Hmin/MN-Hmin
        t[i] = round(ratio*(255-1), 1)
    out_image = t[img2]

    im = Image.fromarray(out_image)
    im.save('hist_equalization.jpeg')
    hist_equal_img = Image.open('hist_equalization.jpeg')
    ratio = float(width)/hist_equal_img.size[0] # 寬300 
    height = int(hist_equal_img.size[1]*ratio) # 以原始比率調整整張大小 
    hist_equal_img = hist_equal_img.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片
    show_hist_equal_img= ImageTk.PhotoImage(hist_equal_img)
    label_Img3= tk.Label(window, image = show_hist_equal_img)
    label_Img3.place(x = 500, y = 80) #第三張圖的位置

    hist_sum = [0] * 256
    image_pix = hist_equal_img.load()

    for i in range(hist_equal_img.size[0]):
        for j in range(hist_equal_img.size[1]):
            hist_sum[image_pix[i, j]] = hist_sum[image_pix[i, j]] + 1

    for i in range(len(hist_sum)):
        hist_sum[i] = round((hist_sum[i] - min(hist_sum))* 600 / max(hist_sum) - min(hist_sum)) #size=600
    image_sum_new = hist_sum

    his = Image.new("L", (512 , 700), 255) #("mode",size) L:灰階
    draw = ImageDraw.Draw(his)
    for i in range(256):
        if(image_sum_new[i]>0):
            draw.line([(i*2,645),(i*2,645-image_sum_new[i])],fill=100,width=2) #xy座標列表, fill=線條顏色, width=線條寬度
        draw.rectangle([(i*2,650),(i*2+2,700)],fill=i)
    
    equal_his = his.resize( (255, 350), Image.BILINEAR )
    show_equal_his = ImageTk.PhotoImage(equal_his)
    label_Img4 = tk.Label(window, image = show_equal_his)
    label_Img4.place(x = 520, y = 400) # 第四張圖的位置

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
    command = Image_histogram)     # 執行open Image_histogram
btn_Open.place(x = 250, y = 20)    # 按鈕位置

# 創建灰階直方圖按鈕
btn_Open = tk.Button(window,
    text = '直方圖均化',      
    width = 13, height = 2,
    command = histogram_equalization)     # 執行open histogram_equalization
btn_Open.place(x = 400, y = 20)    # 按鈕位置

# 運行整體窗口
window.mainloop()