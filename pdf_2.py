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

from googletrans import Translator


class MY_PDF:
    def __init__(self):
        multiprocessing.freeze_support()
        self.set_pdf_dpi()


        return


    def set_pdf_dpi(self,dpi=300):
        self.pdf_dpi = dpi
        self.pdf_size_scale = self.pdf_dpi  / 72

    def open_pdf(self,file_path):
        self.pdfium_pdf = pdfium.PdfDocument(file_path)
        self.pdfplumber_pdf = pdfplumber.open(file_path)

    def get_page_size(self):
        return len(self.pdfium_pdf)

    def get_page_index_list(self):
        return [i for i in range(self.get_page_size())]

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

    def get_page_text(self,page_index):
        page = self.pdfium_pdf.get_page(page_index)
        textpage = page.get_textpage()

        page_text = textpage.get_text()
        return page_text

    def get_page_words(self,page_index):
        page = self.pdfplumber_pdf.pages[page_index]
        words = page.extract_words()
        page_words = []
        for word in words:
            #word_rect = cv2.Rect(word['x0'], word['top'], word['x1'] - word['x0'], word['bottom'] - word['top'])
            word_rect = [word['x0'],word['top'],word['x1'],word['bottom']]
            word_text = word['text']
            page_words.append((page_index,word_rect,word_text))
        return page_words

    def conver_words_box_pos(self,page_words,page_scale):
        page_words_back = []
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect) * page_scale
            word_rect = list(word_rect)
            page_words_back.append((page_index,word_rect,word_text))
        return page_words_back

    def draw_words_and_save(self,image,image_save_path,page_words,page_scale=1):
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect)
            word_rect = word_rect.astype(np.uint32)

            cv2.rectangle(image, (word_rect[0],word_rect[1]),(word_rect[2],word_rect[3]), (0, 0, 255), 1)
        cv2.imwrite(image_save_path,image)

    def tttt(self,path,out_path):
        self.open_pdf(path)
        pdf_page_num = self.get_page_index_list()
        for page_index in pdf_page_num:
            print("[INFO] process pdf page : " + str(page_index))
            page_image = self.get_page_image(page_index)
            page_words = self.get_page_words(page_index)

            page_words = self.conver_words_box_pos(page_words,self.pdf_size_scale)

            path = "pdf_%02d.bmp" % page_index
            save_image_path = os.path.join(out_path,path)
            print(save_image_path)
            self.draw_words_and_save(page_image,save_image_path,page_words)




def auto_create_path(FilePath):
    if os.path.exists(FilePath):
        return
    if os.path.isfile(FilePath):
        FilePath = os.path.dirname(FilePath)
    if os.path.exists(FilePath):
        return
    else:
        os.makedirs(FilePath)


def test():
    filepath = "./datas/example.pdf"
    out_path = "out_put"
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    auto_create_path(out_path)

    pdf = MY_PDF()
    pdf.tttt(filepath,out_path)


test()

