from copy import copy
import cv2
from time import time

from outline import Outline


class Render:
    def __init__(self):
        self.enhanced = None
        self.rectangle = None

        self.hyst1 = 0
        self.hyst2 = 0

        self.template = Outline()
        self.runframe = Outline()

        self.ts = []

    def im_enhancing(self, img, trckbar_locate):

        self.rectangle = None

        self.enhanced = img
        return self.enhanced

    def templ_reg(self, mouse, trckbar_locate):

        event, x, y, status = mouse

        if event == cv2.EVENT_LBUTTONDOWN:
            self.rectangle = x, y, 0, 0
        if status == cv2.EVENT_LBUTTONDOWN and self.rectangle is not None:
            initx, inity, *_ = self.rectangle
            self.rectangle = initx, inity, x - initx, y - inity
        if status == cv2.EVENT_RBUTTONDOWN:
            self.rectangle = None

        trackbar_values = {}
        for trck in trckbar_locate[1].keys():
            trackbar_values[trck] = cv2.getTrackbarPos(trck, trckbar_locate[0])
        self.hyst1 = trackbar_values["hyst1"]
        self.hyst2 = trackbar_values["hyst2"]

        selected = copy(self.enhanced)

        if self.rectangle is not None:
            x, y, w, h, = self.rectangle
            if w > 0 and h > 0:
                cropped = copy(selected[y:y + h, x:x + w])
                self.template.compute(cropped, self.hyst1, self.hyst2)
                selected[y:y + h, x:x + w] = self.template.outpict()
                cv2.rectangle(selected, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return selected

    def templ_tunning(self, mouse):
        event, x, y, status = mouse
        self.template.reorganize()
        if status == cv2.EVENT_LBUTTONDOWN:
            self.template.to_yelow(x, y)
        elif status == cv2.EVENT_RBUTTONDOWN:
            self.template.to_green(x, y)

        return self.template.outpict(gray=True)

    def run(self, img):
        self.runframe.compute(img, self.template.hyst1, self.template.hyst2)

        h, w = self.template.grayimg.shape[0:2]
        methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                   'cv.TM_CCORR_NORMED']

        method = cv2.TM_CCORR
        t = time()
        res = cv2.matchTemplate(self.runframe.boolimg, self.template.boolimg, method)
        self.ts.append(time() - t)
        if len(self.ts) > 100:
            print("matching:", round(max(self.ts), 2))
            self.ts = []

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        x, y = max_loc
        overlayed_value = cv2.countNonZero(cv2.bitwise_and(self.runframe.boolimg[y:y+h, x:x+w], self.template.boolimg))
        full_value = cv2.countNonZero(self.template.boolimg)
        ratio = ((overlayed_value/full_value)*100)
        x, y = x*2, y*2
        if ratio > 40:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        img[y:y+h, x:x+w][self.template.gy, self.template.gx] = color
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

        return img

