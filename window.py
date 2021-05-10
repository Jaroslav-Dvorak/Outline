import cv2
from PIL import ImageTk, Image
from tkinter import Frame, Scrollbar, HORIZONTAL, SUNKEN, E, W, N, S, BOTH, Canvas, ALL, Tk
from time import sleep
#
# class Window:
#     def __init__(self, name, trackbars):
#         self.root = Tk()
#         # setting up a tkinter canvas with scrollbars
#         frame = Frame(self.root, bd=2, relief=SUNKEN)
#         frame.grid_rowconfigure(0, weight=1)
#         frame.grid_columnconfigure(0, weight=1)
#         xscroll = Scrollbar(frame, orient=HORIZONTAL)
#         xscroll.grid(row=1, column=0, sticky=E + W)
#         yscroll = Scrollbar(frame)
#         yscroll.grid(row=0, column=1, sticky=N + S)
#         self.canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
#         self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
#         xscroll.config(command=self.canvas.xview)
#         yscroll.config(command=self.canvas.yview)
#         frame.pack(fill=BOTH, expand=1)
#
#     def view(self, img):
#         img = ImageTk.PhotoImage(image=Image.fromarray(img))
#         self.canvas.create_image(0, 0, image=img, anchor="nw")
#         self.canvas.config(scrollregion=self.canvas.bbox(ALL))
#         self.root.update()
#         sleep(0.025)
#
#     def destroy(self):
#         cv2.destroyWindow(self.winname)
#
#     def mouse_callback(self, event, x, y, status, opt):
#         pass
#
#     def trackbar_callback(self, val):
#         pass
#
#     def keyboard(self, key):
#         pass


class Window:
    def __init__(self, name, trackbars):
        self.winname = name
        cv2.namedWindow(self.winname)
        cv2.moveWindow(self.winname, 20, 20)

        for trck_name, default_val in trackbars.items():
            cv2.createTrackbar(trck_name, self.winname, default_val, 1000, self.trackbar_callback)

        cv2.setMouseCallback(self.winname, self.mouse_callback, 1)

    def view(self, img):
        cv2.imshow(self.winname, img)
        key = cv2.waitKey(5)
        if key > 0:
            self.keyboard(key)

    def destroy(self):
        cv2.destroyWindow(self.winname)

    def mouse_callback(self, event, x, y, status, opt):
        pass

    def trackbar_callback(self, val):
        pass

    def keyboard(self, key):
        pass
