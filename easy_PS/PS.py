# -*- coding: utf-8 -*-
# -*- coding: cp936 -*-
# -*- coding:gbk -*-

import Tkinter
import tkFileDialog
from Tkinter import *
from PIL import Image
import Image, ImageEnhance, ImageDraw, ImageFont
ffilename=''
class MyWindow():
      def __init__(self):
            self.root=Tk()
            self.root.geometry('350x450')
            self.root.title('图像处理系统')
            button1=Button(self.root,text='查看图片',command=onopen,width=40,height=3)
            button2=Button(self.root,text='添加文字',command=onaf,width=40,height=3)
            button3=Button(self.root,text='旋转图片',command=onxz,width=40,height=3)
            button4=Button(self.root,text='缩放图片',command=onsf,width=40,height=3)
            button5=Button(self.root,text='退出',command=self.root.destroy,width=40,height=3)
            button1.pack()
            button2.pack()
            button3.pack()
            button4.pack()
            button5.pack()
def onopen():
            filename=tkFileDialog.askopenfilename()
            #print filename
            if(len(filename) == 0):
                  return 
            filename=filename.replace('/','\\')
            #print filename
            global ffilename
            ffilename=filename
            #filename=tkFileDialog.askopenfilename()
            im=Image.open(filename)
            im.show()
def onsf():
      def onsure():
            x=int(ent1.get())
            y=int(ent2.get())
            smallimg=im.resize((x,y),Image.ANTIALIAS)
            smallimg.save(ent3.get(),"png")
            smallimg.show()
      filename=tkFileDialog.askopenfilename()
      if(len(filename) == 0):
            return 
      im=Image.open(filename)
      sf=Tk()
      sf.title('输入信息')
      frame=Frame(sf)
      frame.pack(padx=8,pady=8,ipadx=4)
      lab1=Label(frame,text='输入长度:')
      lab1.grid(row=0,column=0,padx=5,pady=5,sticky=W)
      
      u=StringVar()
      ent1=Entry(frame,textvariable=u)
      ent1.grid(row=0,column=1,sticky='ew',columnspan=2)
      lab2=Label(frame,text='输入高度:')
      lab2.grid(row=1,column=0,padx=5,pady=5,sticky=W)
      p=StringVar()
      ent2=Entry(frame,textvariable=p)
      ent2.grid(row=1,column=1,sticky='ew',columnspan=2)
      lab3=Label(frame,text='另存为:')
      lab3.grid(row=2,column=0,padx=5,pady=5,sticky=W)
      n=StringVar()
      ent3=Entry(frame,textvariable=n)
      ent3.grid(row=2,column=1,sticky='ew',columnspan=2)
      
      
      button=Button(frame,text='确定',command=onsure, default='active')
      button.grid(row=3,column=1)
      button1=Button(frame,text='退出',command=sf.destroy, default='active')
      button1.grid(row=3,column=2)
      sf.mainloop()

def text2img(text, color='red', dx=25):
    """生成内容为 TEXT 的水印"""
    font_color = color
    font_size=dx
    font = ImageFont.truetype('simsun.ttc', font_size)
    #多行文字处理
    text = text.split('\n')
    mark_width = 0
    for  i in range(len(text)):
        (width, height) = font.getsize(text[i])
        if mark_width < width:
            mark_width = width
    mark_height = height * len(text)

    #生成水印图片
    mark = Image.new('RGBA', (mark_width,mark_height))
    draw = ImageDraw.ImageDraw(mark, "RGBA")
    draw.setfont(font)
    for i in range(len(text)):
        (width, height) = font.getsize(text[i])
        draw.text((0, i*height), text[i], fill=font_color)
    return mark

def set_opacity(im, opacity):
    """设置透明度"""

    assert opacity >=0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, x,y, opacity=1):
    """添加水印"""

    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            print "The mark image size is larger size than original image file."
            return False

        #设置水印位置
        layer = Image.new('RGBA', im.size,)
        layer.paste(mark,(x,y))
        return Image.composite(layer, im, layer)
    except Exception as e:
        print ">>>>>>>>>>> WaterMark EXCEPTION:  " + str(e)
        return False

def onaf():
      def onsure():
            txt=ent1.get()
            x=ent2.get()
            y=ent3.get()
            color=ent5.get()
            dx=ent4.get()
            rename=ent6.get()
            mark = text2img(txt,color,int(dx))
            image = watermark(im, mark, int(x),int(y), 0.9)
            if image:
              image.save(rename,'png')
              image.show()
            else:
              print "Sorry, Failed."
      filename=tkFileDialog.askopenfilename()
      if(len(filename) == 0):
            return 
      im=Image.open(filename)
      sf=Tk()
      sf.title('add font')
      frame=Frame(sf)
      frame.pack(padx=8,pady=8,ipadx=4)
      lab1=Label(frame,text='输入文字')
      lab1.grid(row=0,column=0,padx=5,pady=5,sticky=W)
      u=StringVar()
      ent1=Entry(frame,textvariable=u)
      ent1.grid(row=0,column=1,sticky='ew',columnspan=2)
      
      lab2=Label(frame,text='位置x')
      lab2.grid(row=1,column=0,padx=5,pady=5,sticky=W)
      p=StringVar()
      ent2=Entry(frame,textvariable=p)
      ent2.grid(row=1,column=1,sticky='ew',columnspan=2)
      
      lab3=Label(frame,text='位置y')
      lab3.grid(row=2,column=0,padx=5,pady=5,sticky=W)
      n=StringVar()
      ent3=Entry(frame,textvariable=n)
      ent3.grid(row=2,column=1,sticky='ew',columnspan=2)
      
      lab4=Label(frame,text='字体大小')
      lab4.grid(row=3,column=0,padx=5,pady=5,sticky=W)
      q=StringVar()      
      ent4=Entry(frame,textvariable=q)
      ent4.grid(row=3,column=1,sticky='ew',columnspan=2)

      lab5=Label(frame,text='颜色')
      lab5.grid(row=4,column=0,padx=5,pady=5,sticky=W)
      c=StringVar()
      ent5=Entry(frame,textvariable=c)
      ent5.grid(row=4,column=1,sticky='ew',columnspan=2)
      
      lab6=Label(frame,text='另存为')
      lab6.grid(row=5,column=0,padx=5,pady=5,sticky=W)
      z=StringVar()
      ent6=Entry(frame,textvariable=z)
      ent6.grid(row=5,column=1,sticky='ew',columnspan=2)
      
      
      
      button=Button(frame,text='确定',command=onsure, default='active')
      button.grid(row=6,column=0)
      button1=Button(frame,text='退出',command=sf.destroy, default='active')
      button1.grid(row=6,column=2)
      sf.mainloop()
      
    # text = open('README.md').read().decode('utf-8')
    # print text
def onxz():
      def onsure():
            w=ent1.get()
            q=ent2.get()
            im2=im1.rotate(int(w))
            im2.save(q,'png')
            im2.show()
      filename=tkFileDialog.askopenfilename()
      if(len(filename) == 0):
            return 
      im1=Image.open(filename)      
      ri=Tk()
      frame=Frame(ri)
      ri.title('旋转图片')
      frame.pack(padx=8,pady=8,ipadx=4)
      lab1=Label(frame,text='输入旋转角度')
      lab1.grid(row=0,column=0,padx=5,pady=5,sticky=W)
      u=StringVar()
      ent1=Entry(frame,textvariable=u)
      ent1.grid(row=0,column=1,sticky='ew',columnspan=2)

      lab2=Label(frame,text='命名')
      lab2.grid(row=1,column=0,padx=5,pady=5,sticky=W)
      n=StringVar()
      ent2=Entry(frame,textvariable=n)
      ent2.grid(row=1,column=1,sticky='ew',columnspan=2)
      
      button=Button(frame,text='确定修改',command=onsure, default='active')
      button.grid(row=2,column=1)
      button1=Button(frame,text='退出',command=ri.destroy, default='active')
      button1.grid(row=2,column=2)
      

win = MyWindow()
win.root.mainloop()
