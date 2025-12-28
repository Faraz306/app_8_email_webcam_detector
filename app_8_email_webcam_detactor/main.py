import cv2
import time
from emailing import send_email

time.sleep(1)
video = cv2.VideoCapture(0)
first_frame = None
while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    counters, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for counter in counters:
        if cv2.contourArea(counter) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(counter)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        if rectangle.any():
            status = 1
            send_email()
    status_list = []
    status_list.append(status)
    print(status_list)
    status_list = status_list[-2:]
    if len(status_list) == 2 and status_list[0] == 1 and status_list[1] == 0:
        send_email()

    cv2.imshow('My first frame', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()