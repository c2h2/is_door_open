import cv2
from numpy import *


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

        ret=detect_door(img, 0.04, 0.5, 0.5, 2)
        cv2.imshow('my webcam', ret[1])
    cv2.destroyAllWindows()


def detect_door(img, thresh_percentage, x_start, y_start, diff_value):
    height, width, channels = img.shape
    mask = zeros((height+2, width+2), uint8) # 2 pix wider than org image
    total_pixels = height * width
    thresh = height * width * thresh_percentage
    start_pixel = (int(width*x_start), int(height*y_start))

    lo_diff = (diff_value,)*3
    hi_diff = (diff_value,)*3
    connectivity=4
    
    ret = cv2.floodFill(img, mask, start_pixel, (0,255,0), lo_diff, hi_diff, connectivity)

    #check the size of the floodfilled area, if it's less than thresh, the door is open:
    is_open = ret[0] < thresh

    
    if is_open:
        print("OPEN :" + "{0:.1%}".format(ret[0]/total_pixels))
    else:    
        print("CLOSE:" + "{0:.1%}".format(ret[0]/total_pixels))
    
        
    return (is_open, ret[1])
    #cv2.imwrite(imgFile.replace(".jpg", "") + "_result.jpg", img)


def main():
    show_webcam(mirror=True)

if __name__ == '__main__':
    main()
