#!usr/bin/env python
# _*_ coding: UTF-8 _*_
import cv2
import sys
import os
import numpy as np
import pypdfium2 as pdfium
from multiprocessing import Pool
import multiprocessing
import shutil
import pdfplumber
import pytesseract
from googletrans import Translator


class PDF:
    def __init__(self):
        self.pdf_images = []
        self.page_scale = 300/72
        return
    def create_a4(self):
        pdf = pdfium.PdfDocument.new()
        # a4 2480×3508
        width, height = (595, 842)
        page_a = pdf.new_page(width, height)


    def example(self,filepath):
        # Load a document

        pdf = pdfium.PdfDocument(filepath)

        # render a single page to a PIL image (in this case: the first one)
        page = pdf.get_page(0)

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
            if True :
                break
            print(
                "    " * item.level +
                "[%s] %s -> %s  # %s %s" % (
                    state, item.title, target,
                    pdfium.ViewmodeToStr[item.view_mode],
                    [round(c, n_digits) for c in item.view_pos],
                )
            )

        # Load a text page helper
        textpage = page.get_textpage()

        # Extract text from the whole page
        text_all = textpage.get_text_range()
        print("yhyh123")
        #print(text_all)
        print("yhyh456")
        width, height = page.get_size()
        # Set the absolute page rotation to 90° clockwise
        #page.set_rotation(90)

        # Locate objects on the page
        for obj in page.get_objects():
            print("ppp")
            print("   " * obj.level + pdfium.ObjectTypeToStr[obj.type], obj.get_pos())

        pil_image = page.render_to(pdfium.BitmapConv.pil_image)
        #pil_image.save("output.jpg")
        page.close()
        # a4 2480×3508
        # concurrently render multiple pages to PIL images (in this case: all)
        page_indices = [i for i in range(len(pdf))]
        renderer = pdf.render_to(
            pdfium.BitmapConv.pil_image,
            page_indices=page_indices,
            scale=300 / 72,  # 72dpi resolution
            crop=(0, 0, 0, 0),  # no crop (form: left, right, bottom, top)
            greyscale=False,  # coloured output
            fill_colour=(255, 255, 255, 255),  # fill bitmap with white background before rendering (form: RGBA)
            colour_scheme=None,  # no custom colour scheme
            optimise_mode=pdfium.OptimiseMode.NONE,
            prefer_bgrx=False,
        )
        for image, index in zip(renderer, page_indices):
            #image.save("output_%02d.jpg" % index)
            #print(image.size)
            #print(image.)
            pix = np.array(image.getdata()).reshape(image.size[1], image.size[0], 3)
            pix = pix.astype(np.uint8)
            pix = cv2.cvtColor(pix, cv2.COLOR_BGR2RGB)
            path =  "output_%02d.bmp" % index
            cv2.imwrite(path,pix)
            image.close()

        pdf.close()
    def draw_rect(self,image,rect,page_scale = 1):
        #for rect in rects:
        left, bottom, right, top = rect
        left    *=page_scale
        bottom  *= page_scale
        right   *= page_scale
        top     *= page_scale

        cv2.rectangle(image, (int(left),int(top)),(int(right),int(bottom)), (0, 255, 0), 2)
            #return image
        return image

    def pdf_to_image(self,pdf,index):

        renderer = pdf.render_to(
            pdfium.BitmapConv.numpy_ndarray,
            page_indices=index,
            scale=300 / 72,  # 72dpi resolution
            crop=(0, 0, 0, 0),  # no crop (form: left, right, bottom, top)
            greyscale=False,  # coloured output
            fill_colour=(255, 255, 255, 255),  # fill bitmap with white background before rendering (form: RGBA)
            colour_scheme=None,  # no custom colour scheme
            optimise_mode=pdfium.OptimiseMode.NONE,
            prefer_bgrx=False,
        )
        image = []
        for array, index in zip(renderer, [index]):
            image = array[0]
            image = image.astype(np.uint8)
        return image

    def translate_picture(self,text):
        print(text.replace("\n", " ").split("."))
        split_text = text.replace("\n", " ").split(".")
        for i in split_text:
            if i != "":
                i += "."
                translator = Translator()
                translation = translator.translate(i, dest="zh-CN")
                print(translation.text)

    def extract_text_and_image(self,file_path):
        pdf = pdfium.PdfDocument(file_path)
        print(len(pdf))

        page_indices = [i for i in range(len(pdf))]


        for index in  range(len(pdf)):
            page_string_box = []
            page_images = []
            page_text = []
            page_size = pdf.get_page_size(index)


            page = pdf.get_page(index)
            image = page.render_tonumpy(
                scale= self.page_scale,  # 72dpi resolution
                crop=(0, 0, 0, 0),  # no crop (form: left, right, bottom, top)
                greyscale=False,  # coloured output
                fill_colour=(255, 255, 255, 255),  # fill bitmap with white background before rendering (form: RGBA)
                colour_scheme=None,  # no custom colour scheme
                optimise_mode=pdfium.OptimiseMode.NONE,
                prefer_bgrx=False
            )
            self.pdf_images.append(image[0])


            page_obj = page.get_objects(1)

            for obj in page_obj:
                #print(obj.type)
                if pdfium.ObjectTypeToStr[obj.type] != "text":
                    continue

                #print("   " * obj.level + pdfium.ObjectTypeToStr[obj.type], obj.get_pos())
                #self.draw_rect(image[0],obj.get_pos(),page_scale)


            textpage = page.get_textpage()

            page_text = textpage.get_text()
            #self.translate_picture(page_text)
            print(page_text)

            # Extract text from the whole page
            page_text = textpage.get_text_range()
            #print(page_text)
            #return
            page_text_boxs = textpage.get_rectboxes()
            #for box in page_text_boxs:
            #    print(box)

                #print("   " * obj.level + pdfium.ObjectTypeToStr[obj.type], obj.get_pos())
                #self.draw_rect(image[0],box,page_scale)
            #return

            #for rect, i in zip(page_text_boxs, [index]):
            #    page_string_box.append(rect)


            #print(left)
            #return
            #if 1==1 :
            #    continue



            #self.draw_rect(image[0],page_string_box)

            #cv2.imshow("text",page_images[0])

            path =  "out_put/output_%02d.bmp" % index
            cv2.imwrite(path,image[0])


        pdf.close()

    def test_3(self,path):

        # 读取pdf并选择对应的页数
        pdf = pdfplumber.open(path)
        page = pdf.pages[0]
        #print(page)
        # 提取文本并可视化
        words = page.extract_words()
        #text = page.extract_text()
        print("yhyh")
        #print(text)
        for word in words:
            image = self.pdf_images[0]
            #print(word)
            path =  "out_put/output_%02d.bmp" % 99
            self.draw_rect(image,(word['x0'],word['bottom'],word['x1'],word['top']),self.page_scale)
            cv2.imwrite(path,image)
        #print(words)
        #im = page.to_image()
        #im.draw_rects(words)


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

    pdf = PDF()
    pdf.extract_text_and_image(filepath)
    #pdf.example(filepath)
    pdf.test_3(filepath)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()