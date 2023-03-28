import os
import cv2
import numpy as np
import multiprocessing
import shutil

from pdf_pdfium import  *
from pdf_pdfplumber import  *
from pdf_pdfminer3k import  *


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

    pdf = PDF_pdfium()
    pdf.open(filepath)
    pdf_page_num = pdf.get_page_number()
    page_index = 0
    page_scale = 4
    page_mediabox,scale,image = pdf.get_page_image(page_index,page_scale)

    pdf = PDF_pdfminer3k()
    pdf.open(filepath)
    page_object_text = pdf.get_page_text(page_index)
    for obj in page_object_text:
        obj.draw_box(image,page_scale)

    pdf.auto_save_image(image,out_path,"1.bmp")


test()