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
    pdf = PDF_pdfplumber()
    pdf = PDF_pdfminer3k()
    pdf.open(filepath)
    page_number = pdf.get_page_number()
    print(page_number)
    page_MediaBox = pdf.get_page_MediaBox(0)
    print(page_MediaBox)
    page_MediaBox = pdf.get_page_text(0)
    print(page_MediaBox)


test()