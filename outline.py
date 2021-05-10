from copy import copy
import cv2
import numpy as np

class Outline:
    def __init__(self):
        self.bgrimg = None
        self.grayimg = None
        self.boolimg = None
        self.hyst1, self.hyst2 = 0, 0
        self.gy, self.gx = np.array([], np.uint8), np.array([], np.uint8)
        self.yy, self.yx = np.array([], np.uint8), np.array([], np.uint8)
        self.segmented = False

    def compute(self, img, hyst1, hyst2):
        self.hyst1, self.hyst2 = hyst1, hyst2
        self.bgrimg = img
        self.grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dowscaled = cv2.pyrDown(self.grayimg)
        canny = cv2.Canny(dowscaled, hyst1, hyst2)
        cy, cx = np.where(canny == 255)
        self.boolimg = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        self.boolimg[cy, cx] = 255

        cy, cx = cy*2, cx*2
        for i in range(2):
            cy = np.concatenate((cy, cy + i))
            cx = np.concatenate((cx, cx))
        for i in range(2):
            cy = np.concatenate((cy, cy))
            cx = np.concatenate((cx, cx + i))

        self.gy, self.gx = cy, cx
        self.segmented = False
        return len(cy)

    def outpict(self, gray=False):
        img = copy(self.bgrimg) if not gray else cv2.cvtColor(copy(self.grayimg), cv2.COLOR_GRAY2BGR)
        img[self.gy, self.gx] = (0, 255, 0)
        img[self.yy, self.yx] = (0, 255, 255)
        return img

    def reorganize(self):
        if not self.segmented:
            ncy = np.array([], np.uint8)
            ncx = np.array([], np.uint8)
            numpixel = len(self.gy)//16
            for i in range(numpixel):
                ncy = np.append(ncy, self.gy[i::numpixel])
                ncx = np.append(ncx, self.gx[i::numpixel])

            self.gy, self.gx = ncy, ncx
            self.segmented = True
            print("reorganized")
            return True
        else:
            return False

    def to_yelow(self, x, y):
        gy, gx = np.where(np.all(self.outpict()[y - 5:y + 5, x - 5:x + 5] == (0, 255, 0), axis=-1))
        try:
            gy = gy[0]+y-5
            gx = gx[0]+x-5
        except IndexError:
            return
        else:
            sel = list(zip(self.gy, self.gx)).index((gy, gx))
            self.yy = np.append(self.yy, self.gy[sel:sel + 16])
            self.yx = np.append(self.yx, self.gx[sel:sel + 16])
            self.gy = np.delete(self.gy, np.s_[sel:sel+16])
            self.gx = np.delete(self.gx, np.s_[sel:sel+16])

    def to_green(self, x, y):
        yy, yx = np.where(np.all(self.outpict()[y - 5:y + 5, x - 5:x + 5] == (0, 255, 255), axis=-1))
        try:
            yy = yy[0]+y-5
            yx = yx[0]+x-5
        except IndexError:
            return
        else:
            sel = list(zip(self.yy, self.yx)).index((yy, yx))
            self.gy = np.append(self.gy, self.yy[sel:sel + 16])
            self.gx = np.append(self.gx, self.yx[sel:sel + 16])
            self.yy = np.delete(self.yy, np.s_[sel:sel+16])
            self.yx = np.delete(self.yx, np.s_[sel:sel+16])
