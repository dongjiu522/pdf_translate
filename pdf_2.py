#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import multiprocessing
import pypdfium2 as pdfium
from multiprocessing import Pool

import shutil
import pdfplumber
import pytesseract
from googletrans import Translator


class MY_PDF:
    def __init__(self):
        self.set_pdf_dpi()


        return


    def set_pdf_dpi(self,dpi=300):
        self.pdf_dpi = dpi
        self.pdf_size_scale = self.pdf_dpi  / 72

    def open_pdf(self,file_path):
        self.pdfium_pdf = pdfium.PdfDocument(file_path)
        self.pdfplumber_pdf = pdfplumber.open(file_path)

    def get_page_image(self,page_index):

        page = self.pdfium_pdf.get_page(page_index)
        image = page.render_tonumpy(
            scale=self.pdf_size_scale,  # 72dpi resolution
            crop=(0, 0, 0, 0),  # no crop (form: left, right, bottom, top)
            greyscale=False,  # coloured output
            fill_colour=(255, 255, 255, 255),  # fill bitmap with white background before rendering (form: RGBA)
            colour_scheme=None,  # no custom colour scheme
            optimise_mode=pdfium.OptimiseMode.NONE,
            prefer_bgrx=False
        )
        return image[0]

    def get_page_words(self,page_index):
        page = self.pdfplumber_pdf.pages[page_index]
        words = page.extract_words()
        for word in words:
            word_left_top= cv2.point(word['x0'], word['top'])
            word_right_bottom = cv2.point(word['x1'], word['bottom'])
