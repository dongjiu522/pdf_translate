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


from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator,XMLConverter, HTMLConverter, TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
#from pdfminer.utils import set_debug_logging

class LangeTransformer:
    def __init__(self):
        self.trans = Translator()
        return


    def process(self,text):

        result = self.trans .translate(text, dest='zh-cn', src='en')
        return result

class pdfminer3k:
    def __init__(self):

        return

    def open_pdf(self,path,password = ''):
        with open(path,'rb') as fp:
            self.praser = PDFParser(fp)
            self.doc=PDFDocument(self.praser)

            self.praser.set_document(self.doc)
            #self.doc.set_parser(self.praser)

            self.resources = PDFResourceManager(caching=True)
            # 参数分析器
            self.laparam = LAParams()
            #self.doc.initialize()


            # 页面解释器
            #interpreter = PDFPageInterpreter(resources, device)

    def get_device(self,outfp,type = '',scale = 1,outdir = "./out"):

        if os.path.exists(outdir):
            shutil.rmtree(outdir)


        if type == 'text':
            device = TextConverter(self.resources, outfp, laparams=self.laparam)
        elif type == 'xml':
            device = XMLConverter(self.resources, outfp, laparams=self.laparam, outdir=outdir)
        elif type == 'html':
            device = HTMLConverter(self.resources, outfp, scale=scale, layoutmode='normal',laparams=self.laparam, debug=True)
        elif type == 'tag':
            device = TagExtractor(self.resources, outfp)
        else :
            device = PDFPageAggregator(self.resources, laparams=self.laparam)

        return device


    def process_pdf(self,device):
        interpreter = PDFPageInterpreter(self.resources, device)
        # Process each page contained in the document.
        for (pageno, page) in enumerate(self.doc.get_pages()):
            interpreter.process_page(page)



class MY_PDF:
    def __init__(self):
        multiprocessing.freeze_support()
        self.set_pdf_dpi()
        self.LangeTransformer = LangeTransformer()

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
    #612, 792
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
            word_rect = word_rect * page_scale
            word_rect = word_rect.astype(np.uint32)

            cv2.rectangle(image, (word_rect[0],int(792 * page_scale - word_rect[1])),(word_rect[2],int(792 * page_scale -  word_rect[3])), (0, 0, 255), 1)
        cv2.imwrite(image_save_path,image)
    def text_split(self,text,text_max_num = 200):
        result = []
        #text.
    def tttt(self,path,out_path):
        obj_boxs = self.pdfminer3k_sample(path)
        self.open_pdf(path)
        pdf_page_num = self.get_page_index_list()
        for page_index in pdf_page_num:
            print("[INFO] process pdf page : " + str(page_index))
            page_image = self.get_page_image(page_index)
            page_words = self.get_page_words(page_index)
            page_text  = self.get_page_text(page_index)
            page_words = self.conver_words_box_pos(page_words,self.pdf_size_scale)
            #ret = self.LangeTransformer.process(page_text)
            #print(page_text)
            #print(page_text)
            path = "pdf_%02d.bmp" % page_index
            save_image_path = os.path.join(out_path,path)
            #print(save_image_path)
            print(obj_boxs)
            print(page_index)

            boxs = obj_boxs[page_index]

            self.draw_words_and_save(page_image,save_image_path,boxs,self.pdf_size_scale)



    def pdfminer3k_sample(self,path,password = ''):
            all_boxs = {}

            fp = open(path, 'rb')

            # 从文件句柄创建一个pdf解析对象
            parser = PDFParser(fp)

            #fp.close()
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
                boxs = []
                for obj in layout:

                    if (isinstance(obj, LTTextBoxHorizontal)):
                        text = obj.get_text()
                        box = obj.bbox
                        boxs.append((i, box,text))
                all_boxs[i] = boxs
            fp.close()
            return all_boxs


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
    pdf.open_pdf(filepath)
    pdf.tttt(filepath,out_path)
    #pdf.pdfminer3k_sample(filepath)

    return
    pdf_2 = pdfminer3k()
    pdf_2.open_pdf(filepath)
    out_file = "./out.html"
    outfp = open(out_file,'wb')
    #pdf_2.process_pdf(pdf_2.get_device(outfp,type='html'))
test()

