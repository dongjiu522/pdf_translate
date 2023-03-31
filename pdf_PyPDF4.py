#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import shutil
from PyPDF4 import PdfFileMerger, PdfFileReader

from pdf_base import PDF
from PIL import Image



class pdf_PyPDF4(PDF):
    def __init__(self):
        super().__init__()

        return
    def sample(self,path,password=''):


        return

    def open(self,path,password=''):

        return True

    def get_page_number(self):
        return

    def get_page_MediaBox(self,page_index = 0):

        return True

    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):

        return True

    def get_page_tables(self, page_index):

        return

    def get_page_image(self,page_index,scale = 1):

        return False

    def merge_pdf(self,input_pdf_file_lists,output_pdf_path):
        # 创建一个空的 PDF 文件
        merged_pdf = PdfFileMerger()

        # 循环遍历每个 PDF 文件并添加到合并的 PDF 中
        for file_name in input_pdf_file_lists:
            with open(file_name, 'rb') as pdf_file:
                merged_pdf.append(PdfFileReader(pdf_file))

        # 保存合并后的 PDF 文件
        with open(output_pdf_path, 'wb') as output_file:
            merged_pdf.write(output_file)
        return True

    def save_image_to_pdf(self,page_image,output_pdf_path):

        pdf_output = PdfFileMerger()

        image = Image.fromarray(page_image)

        pdf_output.append(image)

        with open(output_pdf_path, 'wb') as f:
            pdf_output.write(f)

        return True

