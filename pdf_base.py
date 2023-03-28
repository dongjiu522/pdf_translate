#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

import pypdfium2 as pdfium
import multiprocessing
from multiprocessing import Pool

import pdfplumber

from pdfminer.converter import PDFPageAggregator,XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import *
from pdfminer.pdfdevice import PDFDevice,TagExtractor
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser


from googletrans import Translator

class LangeTransformer:
    def __init__(self):
        self.trans = Translator()
        return

    def process_en_to_cn(self,text):
        result = self.trans .translate(text, dest='zh-cn', src='en')
        return result

    def process_cn_to_en(self,text):
        result = self.trans .translate(text, dest='en', src='zh-cn')
        return result

class PDF:
    def __init__(self):

        return

    def sample(self,path,password=''):

        return

    def open(self,path,password=''):

        return

    def get_page_number(self):

        return

    def get_page_MediaBox(self,page_index = 0):

        return


    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):

        return

    def get_page_tables(self, page_index):

        return

    def get_page_images(self, page_index,scale = 1):

        return

    def conver_words_box_pos(self,page_words,page_scale):
        page_words_back = []
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect) * page_scale
            word_rect = list(word_rect)
            page_words_back.append((page_index,word_rect,word_text))
        return page_words_back

    def draw_words_and_save(self,image,image_save_path,image_save_name,page_words,page_scale=1):
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect)
            word_rect = word_rect * page_scale
            word_rect = word_rect.astype(np.uint32)
            cv2.rectangle(image, (word_rect[0],word_rect[1]),(word_rect[2],word_rect[3]), (0, 0, 255), 1)
        self.auto_create_path(image_save_path)
        path = os.path.join(image_save_path,image_save_name)
        cv2.imwrite(path,image)

    def auto_save_image(self,image,path,name):
        self.auto_create_path(path)
        path = os.path.join(path,name)
        cv2.imwrite(path,image)

    def auto_create_path(self,FilePath):
        if os.path.exists(FilePath):
            return
        if os.path.isfile(FilePath):
            FilePath = os.path.dirname(FilePath)
        if os.path.exists(FilePath):
            return
        else:
            os.makedirs(FilePath)


class PDF_Object:
    def __init__(self,page_index,mode,x0,y0,x1,y1,data=None,text=None,image=None):
        self.page_index = page_index
        self.mode = mode

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        #self.x0 = math.floor(x0)
        #self.y0 = math.floor(y0)
        #self.x1 = math.ceil(x1)
        #self.y1 = math.ceil(y1)

        self.data = data
        self.text = text
        self.image = image
        return
    def __del__(self):
        return

    def show_image_info(self, image_array):
        print("show image info :")
        print("* image shape   [c,h,w] = " + str(image_array.shape))
        print("* image element type  = " + str(image_array.dtype))
        print("* image range         = " + "[" + str(np.min(image_array)) + "," + str(np.max(image_array)) + "]")
        print("* image mean          = " + str(np.mean(image_array)))
        print("* image median        = " + str(np.median(image_array)))
        return

    def print(self,page_scale=1):
        print("############## obj start")
        print("[mode] = " + str(self.mode))
        print("[box ]")
        x0, y0, x1, y1 = self.box_mul_scale(page_scale)
        print((x0, y0, x1, y1), sep=' ', end='\n', file=sys.stdout, flush=False)
        print("[data] data = " + str(self.data))
        if self.mode == "image":
            self.show_image_info(self.image)
        else:
            print("[image] image = " + str(self.image))
        print("[text] text = " + str(self.text))
        print("############## obj end")


    def box_mul_scale(self,page_scale):
        #self.x0 = math.floor(x0)
        #self.y0 = math.floor(y0)
        #self.x1 = math.ceil(x1)
        #self.y1 = math.ceil(y1)

        return int(math.floor(self.x0 * page_scale)),\
               int(math.floor(self.y0 * page_scale)),\
               int(math.ceil(self.x1 * page_scale)),\
               int(math.ceil(self.y1 * page_scale))

    def draw_box(self,page_image,page_scale = 1):
        x0,y0,x1,y1 = self.box_mul_scale(page_scale)
        cv2.rectangle(page_image, (x0, y0), (x1, y1), (0, 0, 255), 2)

    def draw_image(self,page_image,page_scale=1):
        if self.mode != "image":
            return
        x0, y0, x1, y1 = self.box_mul_scale(page_scale)
        image_resize = 0
        box_w =  x1 - x0
        box_h =  y1 - y0
        cv2.resize(self.image, image_resize,(box_h,box_w))
        page_image[x0:x1, y0:y1] = image_resize

    def cv2AddChineseText(self,page_image, text, position, textColor="black", textSize=16):
        if (isinstance(page_image, np.ndarray)):  # 判断是否OpenCV图片类型
            page_image = Image.fromarray(cv2.cvtColor(page_image, cv2.COLOR_BGR2RGB))
        # 创建一个可以在给定图像上绘图的对象
        draw = ImageDraw.Draw(page_image)
        # 字体的格式
        fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
        #fontStyle = ImageFont.truetype("STSONG.TTF", textSize, encoding="utf-8")

        # 绘制文本
        draw.text(position, text, textColor, font=fontStyle,spacing=5,align ="left")
        # 转换回OpenCV格式
        return cv2.cvtColor(np.asarray(page_image), cv2.COLOR_RGB2BGR)

    def draw_text(self,page_image,page_scale=1):
        if self.mode != "text":
            return
        x0, y0, x1, y1 = self.box_mul_scale(page_scale)
        return self.cv2AddChineseText(page_image,self.text,(x0,y0))

