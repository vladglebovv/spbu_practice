import cv2
import asyncio
import sys


class FromCamera:

    def __init__(self, id):
        self.cap = cv2.VideoCapture(id)
        self.img = self.cap.read()[1]

    async def get_image(self):
        ret, img = self.cap.read()
        return img
