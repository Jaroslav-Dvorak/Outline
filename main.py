from time import time

from camerastream import CameraStream
from window import Window
from render import Render


class IV(CameraStream, Window, Render):
    def __init__(self, source):
        CameraStream.__init__(self, source)
        Render.__init__(self)

        self.windows = (
            ("image enhancing", {"exposure": 300}),
            ("template registration", {"hyst1": 150, "hyst2": 150}),
            ("template tuning", {"hyst1": 150, "hyst2": 150}, self.templ_tunning),
            ("run", {"OK/NOK": 100}, self.templ_tunning)
                        )
        self.window_number = 0

        Window.__init__(self, self.windows[self.window_number][0], self.windows[self.window_number][1])

        self.mouse = (0, 0, 0, 0)

        self.rectangle = None
        self.r_image_edit = None
        self.r_image = None

        self.loopshow()

    def loopshow(self):
        ts = []
        while True:
            if self.window_number == 0:
                source_frame = self.frame()
                output_frame = self.im_enhancing(source_frame, self.windows[0])
            elif self.window_number == 1:
                output_frame = self.templ_reg(self.mouse, self.windows[1])
            elif self.window_number == 2:
                output_frame = self.templ_tunning(self.mouse)
            elif self.window_number == 3:
                t = time()
                output_frame = self.run(self.frame())
                ts.append(time()-t)
                if len(ts)>100:
                    print("celkem:", round(max(ts),2))
                    ts = []
            self.view(output_frame)

    def window_switcher(self):
        self.destroy()
        Window.__init__(self, self.windows[self.window_number][0], self.windows[self.window_number][1])

    def trackbar_callback(self, val):
        pass

    def mouse_callback(self, event, x, y, status, opt):
        self.mouse = (event, x, y, status)

    def keyboard(self, key):
        if key == 13:    # ENTER
            self.window_number += 1
            self.window_switcher()
        elif key == 8:  # BACKSPACE
            self.window_number -= 1
            self.window_switcher()


iv = IV(0)
# iv = IV("rtsp://192.168.43.1:5554/playlist.m3u")
