#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import sys
import os
import cv2
import numpy as np
import shutil

import pypdfium2 as pdfium
import multiprocessing
from multiprocessing import Pool

from pdf_base import PDF

class PDF_pdfium(PDF):
    def __init__(self):
        super().__init__()
        multiprocessing.freeze_support()

        return
    def sample(self,path,password=''):
        pdf = pdfium.PdfDocument(path,password=password)
        version = pdf.get_version()  # get the PDF standard version
        n_pages = len(pdf)  # get the number of pages in the document

        page_indices = [i for i in range(n_pages)]  # all pages
        renderer = pdf.render(
            pdfium.PdfBitmap.to_numpy,
            page_indices=page_indices,
            scale=300 / 72,  # 300dpi resolution
        )
        out_put_path = "./pdfium_sampe"
        for page_index, image in zip(page_indices, renderer):
            name = "pdf_%02d.bmp" % page_index
            self.auto_save_image(image,out_put_path,name)

        for item in pdf.get_toc():

            if item.n_kids == 0:
                state = "*"
            elif item.is_closed:
                state = "-"
            else:
                state = "+"

            if item.page_index is None:
                target = "?"
            else:
                target = item.page_index + 1

            print(
                "    " * item.level +
                "[%s] %s -> %s  # %s " % (
                    state, item.title, target, item.view_mode,
                )
            )

        page = pdf[0]

        # Get page dimensions in PDF canvas units (1pt->1/72in by default)
        width, height = page.get_size()
        # Set the absolute page rotation to 90° clockwise
        page.set_rotation(90)

        # Locate objects on the page
        for obj in page.get_objects():
            print(obj.level, obj.type, obj.get_pos())

        # Load a text page helper
        textpage = page.get_textpage()

        # Extract text from the whole page
        text_all = textpage.get_text_range()
        # Extract text from a specific rectangular area
        text_part = textpage.get_text_bounded(left=50, bottom=100, right=width - 50, top=height - 100)

        # Locate text on the page
        searcher = textpage.search("something", match_case=False, match_whole_word=False)
        # This will be a list of bounding boxes of the form (left, bottom, right, top)
        first_occurrence = searcher.get_next()

        pdf = pdfium.PdfDocument.new()

        image = pdfium.PdfImage.new(pdf)
        image.load_jpeg("./datas/123.jpg")
        metadata = image.get_metadata()

        matrix = pdfium.PdfMatrix().scale(metadata.width, metadata.height)
        image.set_matrix(matrix)

        page = pdf.new_page(metadata.width, metadata.height)
        page.insert_obj(image)
        page.gen_content()

        # PDF 1.7 standard
        #pdf.save("output.pdf", version=17)

        return

    def open(self,path,password=''):
        self.pdf = pdfium.PdfDocument(path,password=password)
        return True

    def get_page_number(self):
        return len(self.pdf)

    def get_page_MediaBox(self,page_index = 0):
        page = self.pdf.get_page(page_index)
        page_mediabox = page.get_mediabox()
        return page_mediabox

    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):
        page = self.pdf.get_page(page_index)
        textpage = page.get_textpage()

        text = textpage.get_text()
        return text

    def get_page_tables(self, page_index):

        return

    def get_page_image(self,page_index,scale = 1):
        page = self.pdf.get_page(page_index)
        page_mediabox = page.get_mediabox()
        image = page.render_tonumpy(
            scale=scale,  # 72dpi resolution
            crop=(0, 0, 0, 0),  # no crop (form: left, right, bottom, top)
            greyscale=False,  # coloured output
            fill_colour=(255, 255, 255, 255),  # fill bitmap with white background before rendering (form: RGBA)
            colour_scheme=None,  # no custom colour scheme
            optimise_mode=pdfium.OptimiseMode.NONE,
            prefer_bgrx=False
        )
        return page_mediabox,scale,image[0]



