import re
import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import os
import io
from flask import Response
from matplotlib import pyplot as plt

word_path = '/home/lucifer/NHAI/ocr_pdf/flask1/static/word_updated/'
char_path = '/home/lucifer/NHAI/ocr_pdf/flask1/static/char_updated/'
    

def ImagetoText(filename):
    """ Takes image as input and return's text extracted from the given image"""

    pil_img = Image.open(filename)



    opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    custom_config = r'-l hin+eng --oem 3 --psm 6'

    text = pytesseract.image_to_string(opencvImage, config=custom_config)

    return text


def ImagetoCharBoxes(filename):
    pil_img = Image.open(filename)
    opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    boxes = pytesseract.image_to_boxes(opencvImage)
    h, w, c = opencvImage.shape

    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(opencvImage, (int(b[1]), h - int(b[2])), \
            (int(b[3]), h - int(b[3])),\
                (0, 255,0), 2)
    img = Image.fromarray(img, 'RGB')
    img.save(filename.filename)
    

    return filename.filename

def ImagetoWordBoxes(filename):
    # img = cv2.imread(filename)
    pil_img = Image.open(filename).convert('RGB') 

    img = np.array(pil_img) 
    # Convert RGB to BGR 
    img = img[:, :, ::-1].copy() 
    
    # opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['width'][i])
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    b,g,r = cv2.split(img)
    rgb_img = cv2.merge([r,g,b])

    # img = Image.fromarray(img, 'RGB')
    cv2.imwrite(word_path+filename.filename, rgb_img)

    return filename.filename 

def Date_pattern(filename):
    pil_img = Image.open(filename)
    # opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    img = np.array(pil_img) 
    # Convert RGB to BGR 
    image = img[:, :, ::-1].copy() 

    d = pytesseract.image_to_data(image, output_type=Output.DICT)

    date_pattern = '^(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).(19|20)\d\d'

    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            if re.match(date_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])

    # img = Image.fromarray(img, 'RGB')
    cv2.imwrite(char_path+filename.filename.rstrip(".jpg")+"_date.jpg", rgb_img)    

    return filename.filename

def Email_pattern(filename):
    pil_img = Image.open(filename)
    # opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    img = np.array(pil_img) 
    # Convert RGB to BGR 
    image = img[:, :, ::-1].copy() 

    d = pytesseract.image_to_data(image, output_type=Output.DICT)

    date_pattern = '^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'

    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            if re.match(date_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print("Text : ", d['text'][i])

    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])

    # img = Image.fromarray(img, 'RGB')
    cv2.imwrite(char_path+filename.filename, rgb_img)    

    return filename.filename

def PinCode_pattern(filename):
    pil_img = Image.open(filename)
    # opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    img = np.array(pil_img) 
    # Convert RGB to BGR 
    image = img[:, :, ::-1].copy() 

    d = pytesseract.image_to_data(image, output_type=Output.DICT)

    date_pattern = '\b[1-9]{1}[0-9]{2}[0-9]{3}\b'

    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            if re.match(date_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print("Text : ", d['text'][i])

    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])

    # img = Image.fromarray(img, 'RGB')
    cv2.imwrite(char_path+filename.filename, rgb_img)    

    return filename.filename
