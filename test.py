import os
import cv2
import numpy as np
import multiprocessing
import shutil

from pdf_pdfium import  *
from pdf_pdfplumber import  *
from pdf_pdfminer3k import  *
from pdf_PyPDF4 import  *


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
    page_mediabox, scale, image = pdf.get_page_image(page_index, page_scale)


    pdf = PDF_pdfminer3k()
    pdf.open(filepath)
    print(image.shape)
    page_object_text = pdf.get_page_text(page_index)
    image_copy = image.copy()
    image_copy[:] = 255
    print(image_copy.shape)
    image_copy_pil = Image.fromarray(image_copy)

    for obj in page_object_text:
        #image = obj.draw_box(image, page_scale)
        #obj.draw_box_pil(image_copy_pil,page_scale)
        #obj.translate_text()
        obj.draw_text(image_copy_pil,"en",page_scale)
        #break
    image_copy_pil.save(os.path.join(out_path, "1_copy.bmp"))

    pdf.auto_save_image(image,out_path,"1.bmp")
    #pdf.auto_save_image(image_copy, out_path, "1_copy.bmp")

    images = []
    images.append(image.copy())
    images.append(image.copy())
    images.append(image.copy())
    pdf = PDF()
    pdf.images_to_pdf(images,"./datas/out.pdf")

def test_2():
    filepath = "./datas/example.pdf"
    out_path = "out_put"
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    auto_create_path(out_path)

    pdf = PDF_pdfium()
    pdf.open(filepath)
    pdf_page_num = pdf.get_page_number()
    page_index = 0
    page_scale = 1
    page_mediabox, scale, image = pdf.get_page_image(page_index, page_scale)

    pdf = pdf_PyPDF4()
    pdf_encrypted_out = "./datas/example.pdf"
    pdf_img_out = "./datas/imgs.pdf"
    #pdf.encrypted(filepath,pdf_encrypted_out,"123yh")
    imgs = []
    imgs.append(image)
    pdf.append_image_to_pdf(pdf_img_out,imgs,pdf_encrypted_out)

test()
#test_2()