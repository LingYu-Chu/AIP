#創建GUI窗口打開圖像 顯示在窗口中
from PIL import Image, ImageTk # 導入圖像處理函數庫
import tkinter as tk           # 介面
import tkinter.filedialog
import os.path

# 設定窗口大小命名
window = tk.Tk()
window.title('AIP 60847017S')
window.geometry('850x500')
global img_png,image           # 定義img_png
var = tk.StringVar()    
width = 200

# 打開圖像 顯示圖像
def Open_Img():
    global img_png
    filename = tkinter.filedialog.askopenfilename(filetypes=[("Image files",("*.jpg","*.jpeg","*.ppm","*.bmp"))])
    print(filename)
    img = Image.open(filename)
    name = filename.split("/")[-1]
    print(filename.split("/")[-1])

    ratio = float(width)/img.size[0] # 寬300 
    height = int(img.size[1]*ratio) # 以原始比率調整整張大小 
    nim = img.resize( (width, height), Image.BILINEAR ) # 得到新的尺寸圖片
    nim.save( name + "_new.jpg" ) # 儲存新影像

    img_png = ImageTk.PhotoImage(nim)
    label_Img = tk.Label(window, image=img_png)
    label_Img.place(x=100,y=120) # 第一張圖的位置
    label_Img2= tk.Label(window, image=img_png)
    label_Img2.place(x=450,y=120) #第二張圖的位置

    var.set('原影像格式：'+str(img.format)+'  |  影像大小：'+str(img.size)+' → '+str(nim.size))

# 創建打開影像按鈕 
btn_Open = tk.Button(window,
    text='選擇圖像',      
    width=15, height=2,
    command=Open_Img)     # 執行open img
btn_Open.place(x=100, y=20)    # 按鈕位置

Label_Show = tk.Label(window,
    textvariable=var,   # 使用 textvariable 替換 text, 文字可以做變化
    width=45, height=2)
Label_Show.place(x=100, y=70)

# 運行整體窗口
window.mainloop()