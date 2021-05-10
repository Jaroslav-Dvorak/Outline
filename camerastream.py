import cv2


class CameraStream:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                return frame
        self.cap.release()
        print("Error opening video stream or file")
        exit()
