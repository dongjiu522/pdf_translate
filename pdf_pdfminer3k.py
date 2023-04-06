#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import shutil

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator,XMLConverter, HTMLConverter, TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *

from pdf_base import *

class PDF_pdfminer3k(PDF):
    def __init__(self):
        super().__init__()

        return
    def __del__(self):

        return

    def sample(self, path, password=''):

        fp = open(path, 'rb')

        # 从文件句柄创建一个pdf解析对象
        parser = PDFParser(fp)

        # fp.close()
        # 创建pdf文档对象，存储文档结构
        document = PDFDocument(parser, password)

        # 创建一个pdf资源管理对象，存储共享资源
        rsrcmgr = PDFResourceManager()

        laparams = LAParams()

        # 创建一个device对象
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个解释对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 处理包含在文档中的每一页
        pages = PDFPage.create_pages(document)
        for i, page in enumerate(pages):
            interpreter.process_page(page)
            layout = device.get_result()

            for obj in layout:

                if (isinstance(obj, LTTextBoxHorizontal)):
                    text = obj.get_text()
                    box = obj.bbox
                    print(text)
                    print(box)

        fp.close()
        return
    def ppl(self,path,password,mode,page_index,callback):
        pages = []
        #print("[ppl] path = " + str(path))
        with open(path, 'rb') as fp:
            #print("fp = " + str(fp))
            parser = PDFParser(fp)
            document = PDFDocument(parser, password)
            resources = PDFResourceManager()

            laparams = LAParams()

            # 创建一个device对象
            device = PDFPageAggregator(resources, laparams=laparams)

            # 创建一个解释对象
            interpreter = PDFPageInterpreter(resources, device)

            for i, page in enumerate(PDFPage.create_pages(document)):
                pages.append(page)
            return callback(pages,mode,page_index,device,interpreter)

    def call_back_func(self,pages,mode,page_index,device,interpreter):
        if (mode == "open"):
            return True
        elif (mode == "get_page_number"):
            return len(pages)
        elif (mode == "get_page_MediaBox"):
            page = pages[page_index]
            page_mediabox = page.mediabox
            return page_mediabox
        elif (mode == "get_page_text"):
            page = pages[page_index]
            interpreter.process_page(page)
            layout = device.get_result()

            page_mediabox = page.mediabox
            page_mediabox_w = page_mediabox[2]
            page_mediabox_h = page_mediabox[3]

            objs = []
            for obj in layout:
                box = obj.bbox

                x0 = box[0]
                y0 = page_mediabox_h - box[3]
                x1 = box[2]
                y1 = page_mediabox_h - box[1]

                if (isinstance(obj, LTText)):
                    text = obj.get_text()
                    obj = PDF_Object(page_index,"text",\
                                     x0,y0,\
                                     x1,y1,\
                                     data=None,text=text,image=None)
                    objs.append(obj)
            return objs
                #if (isinstance(obj, LTImage)):
                #    image = obj.get_text()
                #    obj = PDF_Object(page_index,"image",\
                #                     x0,y0,\
                #                     x1,y1,\
                #                     data=None,text=None,image=image)
                #    objs.append(obj)

        else:
            return False
        return

    def open(self,path,password=''):
        self.path = path
        self.password = password
        return self.ppl(self.path,self.password,"open",0,self.call_back_func)


    def get_page_number(self):
        return self.ppl(self.path,self.password,"get_page_number",0,self.call_back_func)

    def get_page_MediaBox(self,page_index = 0):
        return self.ppl(self.path, self.password, "get_page_MediaBox", page_index, self.call_back_func)

    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):
        return self.ppl(self.path, self.password, "get_page_text", page_index, self.call_back_func)


    def get_page_tables(self, page_index):

        return

    def get_page_images(self, page_index,scale = 1):

        return

