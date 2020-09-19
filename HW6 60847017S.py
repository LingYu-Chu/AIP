# 創建GUI窗口打開圖像 顯示在窗口中
#encoding: utf-8

from PIL import Image, ImageTk  # 導入圖像處理函數庫
import matplotlib.pyplot as plt  # 繪圖庫
import numpy as np
import tkinter as tk     # 介面
import tkinter.ttk as tt
import tkinter.filedialog
import os.path

# 設定窗口大小命名
window = tk.Tk()
window.title('AIP 60847017S')
window.geometry('900x550')
global img_png, image, nim, show_hist, mask_size            # 定義img_png
var = tk.StringVar()
width = 300

labelTop = tk.Label(window,text = "Mask size ")
labelTop.place(x = 400, y = 22)

variable = tk.StringVar(window)
variable.set("3 x 3") # default value

w = tk.OptionMenu(window, variable, "3 x 3", "5 x 5")
w.place(x = 480, y = 20)

# 打開圖像 顯示圖像
def Open_Img():
    global img_png, nim, img_name, width, height
    filename = tkinter.filedialog.askopenfilename(filetypes = [("Image files", ("*.jpg", "*.jpeg", "*.ppm", "*.bmp"))])
    img_name = os.path.basename(filename)
    print('檔名：' + os.path.basename(filename))
    img = Image.open(filename)
    img2 = img.convert('L') # 轉成灰階 L- 8位像素，黑白

    ratio = float(width)/img.size[0]  # 寬300
    height = int(img2.size[1]*ratio)  # 以原始比率調整整張大小
    nim = img2.resize((width, height), Image.BILINEAR)  # 得到新的尺寸圖片
    width = nim.size[0]
    height = nim.size[1]

    img_png = ImageTk.PhotoImage(nim)
    label_Img = tk.Label(window, image = img_png)
    label_Img.place(x = 100, y = 120)  # 第一張圖的位置

def get_Value33():
    global mask_value, mask_size
    mask_size = 3
    mask_value = np.zeros((3,3))
    mask_value[0][0] = var1.get()
    mask_value[0][1] = var2.get()
    mask_value[0][2] = var3.get()
    mask_value[1][0] = var4.get()
    mask_value[1][1] = var5.get()
    mask_value[1][2] = var6.get()
    mask_value[2][0] = var7.get()
    mask_value[2][1] = var8.get()
    mask_value[2][2] = var9.get()
    print(mask_value)
    convolution()

def mask33():
    global var1, var2, var3, var4, var5, var6, var7, var8, var9
    Enter_mask = tk.Toplevel(window)
    Enter_mask.geometry('250x160')
    Enter_mask.title('Enter 3x3 Mask Values')
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    var4 = tk.StringVar()
    var5 = tk.StringVar()
    var6 = tk.StringVar()
    var7 = tk.StringVar()
    var8 = tk.StringVar()
    var9 = tk.StringVar()
    enter1 = tk.Entry(Enter_mask, width = 5, textvariable = var1).grid(row = 2, column = 0, padx = 15)
    enter2 = tk.Entry(Enter_mask, width = 5, textvariable = var2).grid(row = 2, column = 1, padx = 15)
    enter3 = tk.Entry(Enter_mask, width = 5, textvariable = var3).grid(row = 2, column = 2, padx = 15)
    enter4 = tk.Entry(Enter_mask, width = 5, textvariable = var4).grid(row = 4, column = 0, padx = 15)
    enter5 = tk.Entry(Enter_mask, width = 5, textvariable = var5).grid(row = 4, column = 1, padx = 15)
    enter6 = tk.Entry(Enter_mask, width = 5, textvariable = var6).grid(row = 4, column = 2, padx = 15)
    enter7 = tk.Entry(Enter_mask, width = 5, textvariable = var7).grid(row = 6, column = 0, padx = 15)
    enter8 = tk.Entry(Enter_mask, width = 5, textvariable = var8).grid(row = 6, column = 1, padx = 15)
    enter9 = tk.Entry(Enter_mask, width = 5, textvariable = var9).grid(row = 6, column = 2, padx = 15)
    button_submit = tk.Button(Enter_mask, text = 'Submit', command = lambda: get_Value33()).grid(row = 7, column = 1, pady = 10)

def get_Value55():
    global mask_value, mask_size
    mask_size = 5
    mask_value = np.zeros((5,5))
    mask_value[0][0] = var1.get()
    mask_value[0][1] = var2.get()
    mask_value[0][2] = var3.get()
    mask_value[0][3] = var4.get()
    mask_value[0][4] = var5.get()
    mask_value[1][0] = var6.get()
    mask_value[1][1] = var7.get()
    mask_value[1][2] = var8.get()
    mask_value[1][3] = var9.get()
    mask_value[1][4] = var10.get()
    mask_value[2][0] = var11.get()
    mask_value[2][1] = var12.get()
    mask_value[2][2] = var13.get()
    mask_value[2][3] = var14.get()
    mask_value[2][4] = var15.get()
    mask_value[3][0] = var16.get()
    mask_value[3][1] = var17.get()
    mask_value[3][2] = var18.get()
    mask_value[3][3] = var19.get()
    mask_value[3][4] = var20.get()
    mask_value[4][0] = var21.get()
    mask_value[4][1] = var22.get()
    mask_value[4][2] = var23.get()
    mask_value[4][3] = var24.get()
    mask_value[4][4] = var25.get()
    print(mask_value)
    convolution()

def mask55():
    global var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18,var19,var20,var21,var22,var23,var24,var25
    Enter_mask2 = tk.Toplevel(window)
    Enter_mask2.geometry('450x250')
    Enter_mask2.title('Enter 5x5 Mask Values')
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    var4 = tk.StringVar()
    var5 = tk.StringVar()
    var6 = tk.StringVar()
    var7 = tk.StringVar()
    var8 = tk.StringVar()
    var9 = tk.StringVar()
    var10 = tk.StringVar()
    var11 = tk.StringVar()
    var12 = tk.StringVar()
    var13 = tk.StringVar()
    var14 = tk.StringVar()
    var15 = tk.StringVar()
    var16 = tk.StringVar()
    var17 = tk.StringVar()
    var18 = tk.StringVar()
    var19 = tk.StringVar()
    var20 = tk.StringVar()
    var21 = tk.StringVar()
    var22 = tk.StringVar()
    var23 = tk.StringVar()
    var24 = tk.StringVar()
    var25 = tk.StringVar()
    enter1 = tk.Entry(Enter_mask2, width = 5, textvariable = var1).grid(row = 2, column = 0, padx = 15)
    enter2 = tk.Entry(Enter_mask2, width = 5, textvariable = var2).grid(row = 2, column = 1, padx = 15)
    enter3 = tk.Entry(Enter_mask2, width = 5, textvariable = var3).grid(row = 2, column = 2, padx = 15)
    enter4 = tk.Entry(Enter_mask2, width = 5, textvariable = var4).grid(row = 2, column = 3, padx = 15)
    enter5 = tk.Entry(Enter_mask2, width = 5, textvariable = var5).grid(row = 2, column = 4, padx = 15)
    enter6 = tk.Entry(Enter_mask2, width = 5, textvariable = var6).grid(row = 4, column = 0, padx = 15)
    enter7 = tk.Entry(Enter_mask2, width = 5, textvariable = var7).grid(row = 4, column = 1, padx = 15)
    enter8 = tk.Entry(Enter_mask2, width = 5, textvariable = var8).grid(row = 4, column = 2, padx = 15)
    enter9 = tk.Entry(Enter_mask2, width = 5, textvariable = var9).grid(row = 4, column = 3, padx = 15)
    enter10 = tk.Entry(Enter_mask2, width = 5, textvariable = var10).grid(row = 4, column = 4, padx = 15)
    enter11 = tk.Entry(Enter_mask2, width = 5, textvariable = var11).grid(row = 6, column = 0, padx = 15)
    enter12 = tk.Entry(Enter_mask2, width = 5, textvariable = var12).grid(row = 6, column = 1, padx = 15)
    enter13 = tk.Entry(Enter_mask2, width = 5, textvariable = var13).grid(row = 6, column = 2, padx = 15)
    enter14 = tk.Entry(Enter_mask2, width = 5, textvariable = var14).grid(row = 6, column = 3, padx = 15)
    enter15 = tk.Entry(Enter_mask2, width = 5, textvariable = var15).grid(row = 6, column = 4, padx = 15)
    enter16 = tk.Entry(Enter_mask2, width = 5, textvariable = var16).grid(row = 8, column = 0, padx = 15)
    enter17 = tk.Entry(Enter_mask2, width = 5, textvariable = var17).grid(row = 8, column = 1, padx = 15)
    enter18 = tk.Entry(Enter_mask2, width = 5, textvariable = var18).grid(row = 8, column = 2, padx = 15)
    enter19 = tk.Entry(Enter_mask2, width = 5, textvariable = var19).grid(row = 8, column = 3, padx = 15)
    enter20 = tk.Entry(Enter_mask2, width = 5, textvariable = var20).grid(row = 8, column = 4, padx = 15)
    enter21 = tk.Entry(Enter_mask2, width = 5, textvariable = var21).grid(row = 10, column = 0, padx = 15)
    enter22 = tk.Entry(Enter_mask2, width = 5, textvariable = var22).grid(row = 10, column = 1, padx = 15)
    enter23 = tk.Entry(Enter_mask2, width = 5, textvariable = var23).grid(row = 10, column = 2, padx = 15)
    enter24 = tk.Entry(Enter_mask2, width = 5, textvariable = var24).grid(row = 10, column = 3, padx = 15)
    enter25 = tk.Entry(Enter_mask2, width = 5, textvariable = var25).grid(row = 10, column = 4, padx = 15)
    button_submit = tk.Button(Enter_mask2, text = 'Submit', command = lambda: get_Value55()).grid(row = 11, column = 2, pady = 10)

def convolution():
    global mask_size, mask_value, width, height, nim, conv_show
    im_pixel = np.array(nim)
    out_pixel = np.copy(im_pixel)
    im_pixel = np.pad(im_pixel, mask_size-2, mode, padder = 0) #在外圍加0
    #sum_mask = np.sum(mask_value)
    for i in range(height):
        for j in range(width):
            first = im_pixel[i:i+mask_size, j:j+mask_size]
            cal = np.sum(np.multiply(first, mask_value)) #np可以直接使用multiply做矩陣相乘,但兩個矩陣要相同行列
            if cal < 0:
                out_pixel[i,j] = 0
            elif cal > 255:
                out_pixel[i,j] = 255
            else:
                out_pixel[i,j] = cal
    out_im = Image.fromarray(out_pixel)
    out_im.save('conv.jpeg')
    conv_img = Image.open('conv.jpeg')
    conv_show = ImageTk.PhotoImage(conv_img)
    label_Img2 = tk.Label(window, image = conv_show)
    label_Img2.place(x = 500, y = 120)  # 第二張圖的位置

def mode(vector, pad_width, iaxis, kwargs):  #網路上的定義np.pad
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector

def select_mask():
    print(variable.get())
    if variable.get() == "3 x 3":
        mask33()
    elif variable.get() == "5 x 5":
        mask55()

# 創建打開影像按鈕
btn_Open = tk.Button(window,text = '選擇圖像', width = 13, height = 2, command = Open_Img)     # 執行open img
btn_Open.place(x = 50, y = 20)    # 按鈕位置

# 創建convolution按鈕
btn_Conv = tk.Button(window,text = 'Convolution', width = 13, height = 2, command = select_mask)     # 執行open img
btn_Conv.place(x = 200, y = 20)    # 按鈕位置

Label_Show = tk.Label(window,textvariable = var, width = 70, height = 2)   # 使用 textvariable 替換 text, 文字可以做變化
Label_Show.place(x = 100, y = 70)

# 運行整體窗口
window.mainloop()
