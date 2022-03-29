# LOAD THU VIEN VA MODULE CAN THIET
import cv2
import pytesseract
import sqlite3
import string
import random

#Khởi tạo ID của thẻ từ

def id_generator(size = 6, chars = string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

RFID_IN = id_generator()
print(RFID_IN)

#Khởi tạo database
conn = sqlite3.connect('florentino.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS florentino ')
c.execute('''CREATE TABLE florentino(id INTEGER PRIMARY KEY, rfidCode TEXT, numberPlate TEXT )''')

sensorIn =True; #NẾU THẺ HỢP LỆ VÀ RFID_IN HOẠT ĐỘNG THÌ CHƯƠNG TRÌNH SẼ QUÉT BIỂN SỐ
while sensorIn:

    #DOC HINH ANH - TACH HINH ANH NHAN DIEN
    img = cv2.imread('9.jpg')
    cv2.imshow('Image', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    contours,h = cv2.findContours(thresh,1,2)
    largest_rectangle = [0,0]
    for cnt in contours:
        lenght = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, lenght, True)
        if len(approx)==4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x,y,w,h = cv2.boundingRect(largest_rectangle[1])

    image=img[y:y+h, x:x+w]
    cv2.drawContours(img,[largest_rectangle[1]],0,(0,255,0),8)

    cropped = img[y:y+h, x:x+w]
    cv2.imshow('Dinh vi bien so xe', img)

    cv2.drawContours(img,[largest_rectangle[1]],0,(255,255,255),18)

    #DOC HINH ANH CHUYEN THANH FILE TEXT
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imshow('Crop', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    numberPlate_text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

    first_string = numberPlate_text.split('|')
    second_string = first_string[0]
    third_string = first_string[1].replace("\n","")


    c.execute('INSERT INTO florentino(rfidCode,numberPlate) VALUES (?,?)', [RFID_IN,second_string+third_string])
    conn.commit()
    print("Bien so xe la:")
    print(second_string+third_string)
    RFID_OUT = RFID_IN; #Giả sử thẻ ra giống với thẻ vào
    numberPlateOut = second_string+third_string #Giả sử biển số xe ra giống với biển số xe vào

    c.execute('select id from florentino where rfidCode=? and numberPlate = ?',(RFID_OUT, numberPlateOut))
    output = c.fetchall()
    print(output)
    sensorIn = False;
    cv2.waitKey()


