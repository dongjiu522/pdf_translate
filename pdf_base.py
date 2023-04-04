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
        result = self.trans.translate(text, dest='zh-cn', src='en').text
        return result

    def process_cn_to_en(self,text):
        result = self.trans.translate(text, dest='en', src='zh-cn').text
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

    def image_to_pdf(self,page_image,output_pdf_path):
        if (isinstance(page_image, np.ndarray)):  # 判断是否OpenCV图片类型
            page_image = Image.fromarray(cv2.cvtColor(page_image, cv2.COLOR_BGR2RGB))
        page_image.save(output_pdf_path)

    def images_to_pdf(self,page_images,output_pdf_path):
        image_pdf = 0
        image_list = []

        for i in range(len(list(page_images))):
            page_image = page_images[i]
            if (isinstance(page_image, np.ndarray)):  # 判断是否OpenCV图片类型
                page_image = Image.fromarray(cv2.cvtColor(page_image, cv2.COLOR_BGR2RGB))
            if i == 0 :
                image_pdf = page_image
            else:
                image_list.append(page_image)
        image_pdf.save(output_pdf_path, save_all=True, append_images=image_list)

    def auto_save_image(self,image,path,name):
        self.auto_create_path(path)
        path = os.path.join(path,name)
        cv2.imwrite(path,image)

    def auto_copy_file(self,file,path,name):
        self.auto_create_path(path)
        path = os.path.join(path,name)
        shutil.copyfile(file,path)

    def split_list(self,lst, chunk_size=10):
        """
        将一个大列表拆分成多个小列表
        :param lst: 大列表
        :param chunk_size: 每个小列表的大小，默认为10
        :return: 包含多个小列表的新列表
        """
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

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

    def translate_text(self):
        if not hasattr(self,"translater"):
            self.translater = LangeTransformer()
        self.text = self.translater.process_en_to_cn(self.text)
        print(self.text)

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
        #print("box " + str( (x0, y0)))
        cv2.rectangle(page_image, (x0, y0), (x1, y1), (0, 0, 255), 2)
        return page_image

    def draw_box_pil(self,page_image,page_scale = 1):
        x0,y0,x1,y1 = self.box_mul_scale(page_scale)
        draw = ImageDraw.Draw(page_image)
        draw.rectangle((x0, y0, x1, y1), outline="blue")
        return page_image

    def draw_image(self,page_image,page_scale=1):
        if self.mode != "image":
            return
        x0, y0, x1, y1 = self.box_mul_scale(page_scale)
        image_resize = 0
        box_w =  x1 - x0
        box_h =  y1 - y0
        cv2.resize(self.image, image_resize,(box_h,box_w))
        page_image[x0:x1, y0:y1] = image_resize

    def cv2AddChineseText(self,page_image, text, position,textSize=16,textColor="black"):
        if (isinstance(page_image, np.ndarray)):  # 判断是否OpenCV图片类型
            page_image = Image.fromarray(cv2.cvtColor(page_image, cv2.COLOR_BGR2RGB))
        # 创建一个可以在给定图像上绘图的对象
        draw = ImageDraw.Draw(page_image)
        # 字体的格式
        print("cv2AddChineseText")
        fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
        #fontStyle = ImageFont.truetype("STSONG.TTF", textSize, encoding="utf-8")
        #ImageDraw.textsize()
        # 绘制文本
        #print("position = " + str(position))

        #print("text" + str(position))
        #print("text" + str(position))
        x0 = position[0]
        y0 = position[1]
        x1 = position[2]
        y1 = position[3]
        box_w = x1 - x0
        box_h = y1 - y0

        # 计算文本的宽度和高度
        text_width, text_height = draw.multiline_textsize(text, font=fontStyle)

        # 计算绘制文本时的左上角坐标
        draw_box_x = (box_w - text_width) / 2
        draw_box_y = (box_h - text_height) / 2
        draw_box_x += x0
        draw_box_y += y0
        draw.multiline_text((draw_box_x,draw_box_y), text, textColor, font=fontStyle,spacing=5,align ="left")
        # 转换回OpenCV格式
        draw.rectangle(position, outline="red")
        page_image_text_opencv = cv2.cvtColor(np.asarray(page_image), cv2.COLOR_RGB2BGR)
        print("[draw] draw text done")
        return page_image_text_opencv

    def cv2AddEnglistText(self,page_image, text, position,textSize=16,textColor="black"):
        fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
        return self.draw_text_with_wrap(page_image,position,text,fontStyle,textColor)

    def draw_text_with_wrap(self,page_image_pil, box, text, font, color):
        draw = ImageDraw.Draw(page_image_pil)
        words = text.split()
        lines = []
        line = ""
        draw.rectangle(box, outline="black")
        x0 = box[0]
        y0 = box[1]
        x1 = box[2]
        y1 = box[3]
        box_w = x1 - x0
        box_h = y1 - y0
        for word in words:

            line_and_word = line + " " + word
            line_and_word_size = draw.textsize(line_and_word, font=font)
            if line_and_word_size[0] <= box_w:
                line = line_and_word
                continue

            sub_word_index = -1
            for word_index in range(1, len(word)):
                word1 = word[:word_index]
                word2 = word[word_index:]
                line_text_subword = line + " " + word1
                line_text_subword_size = draw.textsize(line_text_subword, font=font)
                if line_text_subword_size[0] <= box_w:
                    sub_word_index = word_index
                    continue
                else:
                    break
            if sub_word_index != -1 and (sub_word_index > 0 and sub_word_index <= len(word)):
                sub_word1 = word[:sub_word_index]
                sub_word2 = word[sub_word_index:]
                line = line + " " + sub_word1
                lines.append(line)
                line = "-" + sub_word2
            else:
                lines.append(line)
                line = word

        if line:
           lines.append(line)


        y = y1
        for line in lines:
            line_w,line_h = font.getsize(line)
            draw.rectangle((x0,y,x0 +line_w,y + line_h ), outline="red")
            draw.text((x0, y), line, font=font, fill=color)
            y += line_h

        return True

    def draw_text(self,page_image,mode="en",page_scale=1):
        #print(self.mode)
        if self.mode != "text":
            return
        x0, y0, x1, y1 = self.box_mul_scale(page_scale)
        if mode == "en":
            return self.cv2AddEnglistText(page_image,self.text,(x0, y0, x1, y1),textSize=30)
        if mode == "zh":
            return self.cv2AddChineseText(page_image,self.text,(x0, y0, x1, y1),textSize=30)

