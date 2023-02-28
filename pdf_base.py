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

import pdfplumber

from pdfminer.converter import PDFPageAggregator,XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import *
from pdfminer.pdfdevice import PDFDevice,TagExtractor
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser


from googletrans import Translator


class PDF:
    def __init__(self):

        return

    def sample(self,path,password=''):

        return

    def open(self,path,password=''):

        return

    def get_page_number(self):

        return

    def get_page_MediaBox(self,page_index = 0):

        return


    def get_page_chars(self,page_index):

        return

    def get_page_words(self,page_index):

        return

    def get_page_text(self, page_index):

        return

    def get_page_tables(self, page_index):

        return

    def get_page_images(self, page_index,scale = 1):

        return

    def conver_words_box_pos(self,page_words,page_scale):
        page_words_back = []
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect) * page_scale
            word_rect = list(word_rect)
            page_words_back.append((page_index,word_rect,word_text))
        return page_words_back

    def draw_words_and_save(self,image,image_save_path,image_save_name,page_words,page_scale=1):
        for word in page_words:
            page_index, word_rect, word_text = word
            word_rect = np.array(word_rect)
            word_rect = word_rect * page_scale
            word_rect = word_rect.astype(np.uint32)
            cv2.rectangle(image, (word_rect[0],word_rect[1]),(word_rect[2],word_rect[3]), (0, 0, 255), 1)
        self.auto_create_path(image_save_path)
        path = os.path.join(image_save_path,image_save_name)
        cv2.imwrite(path,image)

    def auto_save_image(self,image,path,name):
        self.auto_create_path(path)
        path = os.path.join(path,name)
        cv2.imwrite(path,image)

    def auto_create_path(self,FilePath):
        if os.path.exists(FilePath):
            return
        if os.path.isfile(FilePath):
            FilePath = os.path.dirname(FilePath)
        if os.path.exists(FilePath):
            return
        else:
            os.makedirs(FilePath)


class PDF_pdfium(PDF):
    def __init__(self):
        super().__init__()

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

    pdf = PDF_pdfminer3k()
    #pdf = PDF_pdfium()
    #pdf.sample(filepath)
    pdf.open(filepath)
    page_number = pdf.get_page_number()
    print(page_number)
    MediaBox = pdf.get_page_MediaBox()
    print(MediaBox)

    page_text = pdf.get_page_text(0)
    print(page_text)

test()