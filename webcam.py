import glob
import os

import cv2
import time
from send_mail import sendmail
from threading import Thread


def clean_images():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


img = ""
video = cv2.VideoCapture(0)
time.sleep(1)
first = None
count = 1
status_list = [0,0]
while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gau = cv2.GaussianBlur(gray, (21, 21), 0)
    status = 0
    if first is None:
        first = gray_gau
    delta = cv2.absdiff(first, gray_gau)
    thresh = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    dil = cv2.dilate(thresh, None, iterations=2)
    contours, check = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 2000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        print(rect.any())
        if rect.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            img = all_images[index]
        else:
            status = 0
    print(status)
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=sendmail, args=(img,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_images)
        clean_thread.daemon = True
        email_thread.start()
    # print(status_list)
    cv2.imshow("My Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
video.release()
clean_thread.start()