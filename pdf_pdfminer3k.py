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

from pdf_base import PDF

class PDF_pdfminer3k(PDF):
    def __init__(self):
        super().__init__()

        return
    def __del__(self):

        self.fp.close()

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

    def open(self,path,password=''):
        self.fp = open(path, 'rb')

        self.parser = PDFParser(self.fp)

        self.document = PDFDocument(self.parser, password)


        self.resources = PDFResourceManager()

        self.laparams = LAParams()

        # 创建一个device对象
        self.device = PDFPageAggregator(self.resources, laparams= self.laparams)

        # 创建一个解释对象
        self.interpreter = PDFPageInterpreter(self.resources, self.device)

        # 处理包含在文档中的每一页
        self.pages = []
        for i, page in enumerate(PDFPage.create_pages(self.document)):
            self.pages.append(page)


        return True


    def get_page_number(self):
        return len(self.pages)

    def get_page_MediaBox(self,page_index = 0):
        page = self.pages[page_index]
        page_mediabox = page.mediabox
        return page_mediabox

    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):
        page = self.pages[page_index]
        self.interpreter.process_page(page)
        layout = self.device.get_result()
        for obj in layout:

            if (isinstance(obj, LTTextBoxHorizontal)):
                text = obj.get_text()
                box = obj.bbox
                print(box)
        return

    def get_page_tables(self, page_index):

        return

    def get_page_images(self, page_index,scale = 1):

        return

