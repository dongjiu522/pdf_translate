import sys
import os
import cv2
import numpy as np
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

def draw_text_with_wrap(image, box,text, font, color):
    draw = ImageDraw.Draw(image)
    words = text.split()
    lines = []
    line = ""
    draw.rectangle(box, outline="red")
    x0 = box[0]
    y0 = box[1]
    x1 = box[2]
    y1 = box[3]
    box_w = x1 - x0
    box_h = y1 - y0
    for word in words:

        line_and_word = line + " " + word
        line_and_word_size = draw.textsize(line_and_word, font=font)
        if line_and_word_size[0] <= box_w:
            line = line_and_word
            continue

        sub_word_index = -1
        for word_index in range(1,len(word)):
            word1 = word[:word_index]
            word2 = word[word_index:]
            line_text_subword = line  + " " +  word1
            line_text_subword_size = draw.textsize(line_text_subword, font=font)
            if line_text_subword_size[0] <= box_w:
                sub_word_index = word_index
                continue
            else:
                break
        if sub_word_index != -1 and (sub_word_index > 0 and sub_word_index <= len(word)):
            sub_word1 = word[:sub_word_index]
            sub_word2 = word[sub_word_index:]
            line = line + " " + sub_word1
            lines.append(line)
            line = "-" + sub_word2
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)
    y = box[1]
    for line in lines:
        draw.text((box[0], y), line, font=font, fill=color)
        y += font.getsize(line)[1]


# 测试代码
image = Image.new("RGB", (1000, 1000), (255, 255, 255))
font = ImageFont.truetype("STSONG.TTF", 20)
text = "This is a long text that needs to be wrapped in a box."
text = "We make a number of contributions: first, we introduce a \n \
model to classify a pet breed automatically from an image. \
The model combines shape, captured by a deformable part\
model detecting the pet face, and appearance, captured by\
a bag-of-words model that describes the pet fur. Fitting the\
model involves automatically segmenting the animal in the\
image. Second, we compare two classification approaches:\
a hierarchical one, in which a pet is first assigned to the cat\
or dog family and then to a breed, and a flat one, in which\
the breed is obtained directly. We also investigate a number\
of animal and image orientated spatial layouts."
box = (200, 200, 800, 800)
draw_text_with_wrap(image, box,text, font, (0, 0, 0))
image.show()





