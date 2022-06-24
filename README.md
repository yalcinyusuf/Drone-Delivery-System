# Drone-Delivery-System
This project is my graduation thesis project. The aim of the studies carried out within the scope of this graduation project is to realize the backbone of the drone delivery system. In this context, studies in which deep learning and drone are integrated were carried out in the project. A QR code confirmation is required to confirm delivery by drone. For this, a data set consisting of QR codes was prepared and the model was trained to recognize the QR code.  
### Dataset
For the training of the model, a QR code data set consisting of 116 data and 1 class was prepared. Help was taken from the data set in the link below.

http://www.fit.vutbr.cz/research/groups/graph/pclines/pub_page.php?id=2012-SCCG-QRtiles

### Model Training

Google Colabratory, which offers Nvidia Tesla K80 GPU support, was used for the training process. YOLOv4 object detection algorithm was used for the model. The OpenCV library was used to perform object recognition with the YOLOv4 algorithm. YOLOv4 is in a very good position compared to its competitors in object detection. YOLO is an algorithm for object detection using convolutional neural networks (CNN). It can detect very quickly and in one go.

You can look at the [QRcode_model.ipynb](https://github.com/yalcinyusuf/Drone-Delivery-System/blob/main/QRcode_model.ipynb) file.

### QR Code Decoding

The pyzbar library, a ready-made Python library, was used for QR decoding. ZBar is an open source software package for reading barcodes and QR codes from various sources such as video streams, image files.

### Drone For Delivery

DJI Tello drone was used as the drone and integrated into the Python code. In this way, streaming was provided through the drone camera and these technologies were enabled to work together. Tello drone can take photo and video recordings. Connection with the drone is carried out via Wi-Fi.

As a result, in this graduation project, the drone takes off when the QR code is read and the match is matched. Likewise, if it fits with the match in hand, it makes the landing and delivery. 

## Results
The avg loss value of the model is 0.3064, and the mAP value is 91.4%. These results enable the model to make successful detections. Thanks to object detection algorithms using deep learning algorithms, drones can detect quickly and be delivered by air in a faster, safer and least costly way. Thus, drones can take part in delivery instead of humans.


Practice example for take off screen:

https://user-images.githubusercontent.com/61952281/175562308-a1d4fb2c-e9d3-4a27-9d24-be3b1b7579bc.mp4


