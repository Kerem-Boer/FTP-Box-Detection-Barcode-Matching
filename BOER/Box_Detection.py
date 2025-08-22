import os
import cv2
from ultralytics import YOLO

global confidence_threshold

# Modeli yükle
def initialize_model(path):
    global model
    model = YOLO(path)
    global labels
    labels = model.names

def set_confidence_threshold(threshold):
    global confidence_threshold
    confidence_threshold = threshold

class Box:
    def __init__(self, coordinates, name, confidence, childs=None):
        self.coordinates = coordinates
        self.name = name
        self.confidence = confidence
        self.childs = childs if childs is not None else []

    def __str__(self):
        return f"Box(name={self.name}, confidence={self.confidence}, coordinates={self.coordinates}, childs={self.childs})"

    def add_child(self, child_box):
        self.childs.append(child_box)

Boxes = []

def Detect_Boxes(frame):
    result = model(frame, verbose=False)[0]

    for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
        if conf.item() < confidence_threshold:
            continue

        coords = box.cpu().numpy().squeeze().astype(int)
        class_name = labels[int(cls.item())]

        box_obj = Box(coordinates=coords, name=class_name, confidence=round(conf.item() * 100, 2))
        Boxes.append(box_obj)

    print(f"{len(Boxes)} boxes detected.")

def Draw_Boxes(frame, boxes):
    bbox_colors = [(164, 120, 87), (68, 148, 228), (93, 97, 209), (178, 182, 133)]

    for i, box in enumerate(boxes):
        color = bbox_colors[i % len(bbox_colors)]
        x1, y1, x2, y2 = box.coordinates

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f'{box.name}: {box.confidence}%'
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    print(f"{len(Boxes)} boxes drawn.")
    return frame

def Export_Box_Coordinates(Boxes, output_file):
    output_file = output_file.replace(".jpg", ".txt")
    with open(output_file, 'w') as f:
        for box in Boxes:
            f.write(f"{box.name};{box.confidence};{box.coordinates[0]},{box.coordinates[1]};{box.coordinates[2]},{box.coordinates[3]}\n")
    print(f"Boxes' data has been written to: {output_file}")