import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
from dotenv import load_dotenv

import uuid
import json
import time
import cv2
import requests
import copy
import os


class Clova_OCR:
    def __init__(self):
        load_dotenv()
        self.api_url = os.getenv("CLOVA_URL")
        self.secret_key = os.getenv("CLOVA_KEY")
        self.request_json = {
            "images": [{"format": "jpg", "name": "demo"}],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(round(time.time() * 1000)),
        }
        self.payload = {"message": json.dumps(self.request_json).encode("UTF-8")}
        self.headers = {"X-OCR-SECRET": self.secret_key}

    def request(self, image):
        # files =  [('file', open(image_path,'rb'))]
        files = [("file", image)]

        response = requests.request(
            "POST", self.api_url, headers=self.headers, data=self.payload, files=files
        )
        result = response.json()
        result_orga = {}
        for idx, field in enumerate(result["images"][0]["fields"]):
            topLeft = [int(x) for x in field["boundingPoly"]["vertices"][0].values()]
            bottomRight = [
                int(x) for x in field["boundingPoly"]["vertices"][2].values()
            ]
            inferText = field["inferText"]
            result_orga[idx] = [topLeft, bottomRight, inferText, set({idx})]
        return result, result_orga

    # tuplify
    def tup(self, point):
        return (point[0], point[1])

    # returns true if the two boxes overlap
    def overlap(self, source, target):
        # unpack points
        tl1, br1 = source
        tl2, br2 = target

        # checks
        if tl1[0] >= br2[0] or tl2[0] >= br1[0]:
            return False
        if tl1[1] >= br2[1] or tl2[1] >= br1[1]:
            return False
        return True

    # returns all overlapping boxes
    def getAllOverlaps(self, boxes, bounds, index):
        ori_overlaps = set()
        overlaps = []
        for a in range(len(boxes)):
            if a != index:
                if self.overlap(bounds, boxes[a][:2]):
                    ori_overlaps.update(boxes[a][3])
                    overlaps.append(a)
        return overlaps, ori_overlaps

    def merge_box(self, result_orga):
        boxes = list(copy.deepcopy(result_orga).values())
        # go through the boxes and start merging
        merge_margin = 15
        finished = False
        while not finished:
            # set end con
            finished = True

            # draw boxes # comment this section out to run faster
            index = len(boxes) - 1
            while index >= 0:
                # grab current box
                curr = boxes[index]
                # add margin
                tl = curr[0][:]
                br = curr[1][:]
                tl[0] -= merge_margin
                tl[1] -= merge_margin
                br[0] += merge_margin
                br[1] += merge_margin
                id = curr[3]
                # get matching boxes
                overlaps, ori_overlaps = self.getAllOverlaps(boxes, [tl, br], index)

                # check if empty
                if len(overlaps) > 0:
                    # combine boxes
                    # convert to a contour
                    con = []
                    con_num = set()
                    ori_overlaps.update(id)
                    overlaps.append(index)
                    for ind in overlaps:
                        tl, br, _, num = boxes[ind]
                        con.append([tl])
                        con.append([br])
                        con_num.update(num)
                    con = np.array(con)

                    # get bounding rect
                    x, y, w, h = cv2.boundingRect(con)
                    # stop growing
                    w -= 1
                    h -= 1
                    merged = [[x, y], [x + w, y + h], "", con_num]

                    # remove boxes from lists
                    overlaps = sorted(list(overlaps), reverse=True)
                    for ind in overlaps:
                        del boxes[ind]
                    boxes.append(merged)

                    # set flag
                    finished = False
                    break
                # increment
                index -= 1

        for box in boxes:
            merged_list = sorted(box[3])
            infer_texts = []
            for idx in merged_list:
                infer_texts.append(result_orga[idx][2])
            box[2] = " ".join(infer_texts)

        return [[x[0], x[1], x[2]] for x in boxes]

    def ocr(self, image):
        result, result_orga = self.request(image)
        merged_boxes = self.merge_box(result_orga)
        return merged_boxes
