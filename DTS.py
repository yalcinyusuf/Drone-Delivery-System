"""
@author:Yusuf
"""

import cv2
import numpy as np
from pyzbar import pyzbar
from djitellopy import Tello
import time


tello = Tello()
tello.connect()

tello.streamon()

def oku():
    teslimat_id = int(input("6 haneli teslimat id giriniz: "))
    while (len(str(teslimat_id)) != 6):
        teslimat_id = int(input("Lütfen 6 haneli teslimat id giriniz: "))
        if (len(str(teslimat_id)) == 6):
            break


    arrQRcode = list()
    lastFrames = list()
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = tello.get_frame_read()
    while True:
        #ret, frame = cap.read()
        frame = cap.frame
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        frame_blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)
        labels = ["Qr code"]

        # Renkleri ayarlama
        colors = ["0,0,255", "0,0,255", "255,0,0", "255,255,0", "0,255,0"]
        colors = [np.array(color.split(",")).astype("int") for color in colors]
        colors = np.array(colors)
        colors = np.tile(colors, (18, 1))
        #  Modele verme, çıktı katmanları ayarlama
        model = cv2.dnn.readNetFromDarknet(r"C:\Users\yusuf\PycharmProjects\Final_Project\pretrained_model_QR\QR_yolov4.cfg",r"C:\Users\yusuf\PycharmProjects\Final_Project\pretrained_model_QR\QR_yolov4_last.weights")
        layers = model.getLayerNames()
        output_layer = [layers[layer - 1] for layer in model.getUnconnectedOutLayers()]

        model.setInput(frame_blob)

        detection_layers = model.forward(output_layer)

        ############## NON-MAXIMUM SUPPRESSION - OPERATION 1 ###################

        ids_list = []
        boxes_list = []
        confidences_list = []

        ############################ END OF OPERATION 1 ########################

        for detection_layer in detection_layers:
            for object_detection in detection_layer:

                scores = object_detection[5:]
                predicted_id = np.argmax(scores)
                confidence = scores[predicted_id]

                if confidence > 0.20:
                    label = labels[predicted_id]
                    bounding_box = object_detection[0:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                    (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")

                    start_x = int(box_center_x - (box_width / 2))
                    start_y = int(box_center_y - (box_height / 2))

                    ############## NON-MAXIMUM SUPPRESSION - OPERATION 2 ###################

                    ids_list.append(predicted_id)
                    confidences_list.append(float(confidence))
                    boxes_list.append([start_x, start_y, int(box_width), int(box_height)])

                    ############################ END OF OPERATION 2 ########################

        ############## NON-MAXIMUM SUPPRESSION - OPERATION 3 ###################

        max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)

        for max_id in max_ids:
            max_class_id = max_ids[0]
            box = boxes_list[max_class_id]

            start_x = box[0]
            start_y = box[1]
            box_width = box[2]
            box_height = box[3]

            predicted_id = ids_list[max_class_id]
            label = labels[predicted_id]
            confidence = confidences_list[max_class_id]

            ############################ END OF OPERATION 3 ########################

            end_x = start_x + box_width
            end_y = start_y + box_height

            box_color = colors[predicted_id]
            box_color = [int(each) for each in box_color]

            label = "{}: {:.2f}%".format(label, confidence * 100)
            QRcodes = pyzbar.decode(frame)
            for qr in QRcodes:
                lastFrames.append(frame)
                qrData = qr.data.decode("utf-8")
                qrType = qr.type
                arrQRcode.append((qrType, qrData))
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)
                cv2.rectangle(frame, (start_x - 1, start_y), (end_x + 1, start_y - 30), box_color, -1)
                cv2.putText(frame, label, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("Drone", frame)

        k = cv2.waitKey(1) & 0xFF
        if len(arrQRcode) != 0 or k == ord("q"):
            break

    cv2.destroyAllWindows()
    if (teslimat_id == int(arrQRcode[0][1])):
        return True
    else:
        return False


def kalkis():
    if oku() == True:
        tello.takeoff()
        inis()
        return True
    else:
        print("Kalkış Eşleşmesi bulunamadı. ")
        return False
def inis():
    if oku() == True:
        print ("İniyor")
        tello.land()
        return True
    else:
        print("İniş Eşleşmesi bulunamadı. ")
        return False


kalkis()
time.sleep(2)
tello.end()
