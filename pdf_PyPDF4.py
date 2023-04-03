#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import shutil
from PyPDF4 import PdfFileMerger, PdfFileReader,PdfFileWriter

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

    def append_image_to_pdf(self,output_pdf_path,page_images,intput_pdf_path=None):
        current_work_dir = os.path.dirname(__file__)
        current_abs_path = os.path.abspath(current_work_dir)
        work_abs_path = os.path.join(current_abs_path,"pdf_append_image")
        if os.path.exists(work_abs_path):
            shutil.rmtree(work_abs_path)

        self.auto_create_path(work_abs_path)

        page_images_batch = self.split_list(page_images,5)

        work_tmp_pdf_path = os.path.join(work_abs_path,"branch_images.pdf")
        work_pdf_path_mr_in = os.path.join(work_abs_path, "mr_in.pdf")
        work_pdf_path_mr_out = os.path.join(work_abs_path, "mr_out.pdf")

        if os.path.exists(work_abs_path):
            shutil.rmtree(work_abs_path)
        self.auto_create_path(work_abs_path)

        if (intput_pdf_path != None) and (os.path.exists(intput_pdf_path)):
            shutil.copyfile(intput_pdf_path,work_pdf_path_mr_in)

        for branch_images in page_images_batch:
            is_mr_pdf_exists = os.path.exists(work_pdf_path_mr_in)
            branch_images_num = len(branch_images)
            if is_mr_pdf_exists == False:
                if branch_images_num == 1:
                    self.image_to_pdf(branch_images[0],work_pdf_path_mr_in)
                else:
                    self.images_to_pdf(branch_images,work_pdf_path_mr_in)
            else:
                if branch_images_num == 1:
                    self.image_to_pdf(branch_images[0], work_tmp_pdf_path)
                else:
                    self.images_to_pdf(branch_images,work_tmp_pdf_path)
                input_pdf_file_lists = []
                input_pdf_file_lists.append(work_pdf_path_mr_in)
                input_pdf_file_lists.append(work_tmp_pdf_path)
                self.merge_pdf(input_pdf_file_lists,work_pdf_path_mr_out)
                os.remove(work_pdf_path_mr_in)
                os.remove(work_tmp_pdf_path)
                os.rename(work_pdf_path_mr_out,work_pdf_path_mr_in)

        path,name = os.path.split(output_pdf_path)
        self.auto_copy_file(work_pdf_path_mr_in,path,name)
        if os.path.exists(work_abs_path):
            shutil.rmtree(work_abs_path)
        return True

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

    def encrypted(self,input_pdf_path,output_pdf_path,pass_word):
        pdf_writer = PdfFileWriter()

        # Open the file and add its pages to pdf_writer
        with open(input_pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

        # Encrypt the PDF with a password
            pdf_writer.encrypt(pass_word)

        # Write the encrypted PDF to a file
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)

        return True


    def add_watermark(self,input_pdf, output_pdf, watermark):

        # reads the watermark pdf file through
        # PdfFileReader
        watermark_instance = PdfFileReader(watermark)

        # fetches the respective page of
        # watermark(1st page)
        watermark_page = watermark_instance.getPage(0)

        # reads the input pdf file
        pdf_reader = PdfFileReader(input_pdf)

        # It creates a pdf writer object for the
        # output file
        pdf_writer = PdfFileWriter()

        # iterates through the original pdf to
        # merge watermarks
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)

            # will overlay the watermark_page on top
            # of the current page.
            page.mergePage(watermark_page)

            # add that newly merged page to the
            # pdf_writer object.
            pdf_writer.addPage(page)

        with open(output_pdf, 'wb') as out:
            # writes to the respective output_pdf provided
            pdf_writer.write(out)
