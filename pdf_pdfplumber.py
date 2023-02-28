#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import shutil

import pdfplumber

from pdf_base import PDF


class PDF_pdfplumber(PDF):
    def __init__(self):
        super().__init__()

        return
    def sample(self,path,password=''):
        pdf = pdfplumber.open(path)
        page01 = pdf.pages[0]  # 指定页码
        text = page01.extract_text()
        table1 = page01.extract_table()  # 提取单个表格
        tables = page01.extract_tables()#提取多个表格
        print(table1)
        return

    def open(self,path,password=''):
        self.pdf = pdfplumber.open(path)
        return True

    def get_page_number(self):

        return len(self.pdf.pages)


    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):
        page = self.pdf.pages[page_index]
        words = page.extract_words()
        page_words = []
        for word in words:
            word_rect = [word['x0'],word['top'],word['x1'],word['bottom']] ## x0,y0,x1,y1
            word_text = word['text']
            page_words.append((page_index,word_rect,word_text))
        return page_words

    def get_page_text(self, page_index):

        return

    def get_page_tables(self, page_index):

        return

    def get_page_images(self, page_index,scale = 1):

        return


