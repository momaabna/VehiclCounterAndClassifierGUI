intervals = (
    (':', 604800),  # 60 * 60 * 24 * 7
    (':', 86400),    # 60 * 60 * 24
    (':', 3600),    # 60 * 60
    (':', 60),
    ('', 1),
    )

def display_time(seconds, granularity=5):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count

            result.append("{}{}".format(value, name))
        else:
            result.append("{}{}".format('00', name))

    return ''.join(result[:granularity])

def start_classify():
    f=1
    import time
    while (f==1):
        time.sleep(1)
        with open('clossify','r') as fi:
            f=int(fi.read())
            fi.close()
    with open('clossify','w') as fi:
            fi.write('1')
            fi.close()
def stop_classify():
    with open('clossify','w') as fi:
            fi.write('0')
            fi.close()
import cv2
import numpy as np

drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
line = list()


# mouse callback function
def interactive_drawing(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN and drawing == False:
        drawing = True
        ix, iy = x, y
        line.append([x, y])
        if not len(line) % 2 :
            cv2.line(img, (line[-2][0], line[-2][1]), (line[-1][0], line[-1][1]), (0, 255, 0), 1)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
img = np.zeros((512, 512, 3), np.uint8)
def dividers(n):
    global line

    cv2.namedWindow('Window')
    cv2.setMouseCallback('Window', interactive_drawing)
    while (len(line)<=2*n):
        cv2.imshow('Window', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 13:
            return line

    cv2.destroyAllWindows()
    return line






