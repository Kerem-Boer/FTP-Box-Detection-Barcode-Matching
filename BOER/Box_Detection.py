import os
import cv2
# from matplotlib import image
from ultralytics import YOLO
import Dynamsoft

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

def Open_Image(image_path):
    if not os.path.exists(image_path):
        print(f"Can not find image: {image_path}")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None
    print(f"Image opened: {image_path}")
    return image

def Crop_Image(image, Boxes,):
    for i, box in enumerate(Boxes):
        x1, y1, x2, y2 = box.coordinates
        cropped = image[y1:y2, x1:x2]
        cv2.imwrite(f"Cropped_Image_{i}.jpg", cropped)

def Complex_Draw_Box(image,items,box):
    for item in items:
        quad = item.get_location()
        x1, y1, x2, y2 = box.coordinates
        new_x1, new_y1 = x1 + quad.points[0].x, y1 + quad.points[0].y
        new_x2, new_y2 = x1 + quad.points[2].x, y1 + quad.points[2].y
        cv2.rectangle(image, (new_x1, new_y1), (new_x2, new_y2), (255, 0, 0), 2)
    cv2.imwrite("output.jpg", image)
    print("Drawed Cx Boxes")

def Add_Child_Barcode(items, box):
    for item in items:
        mid_point = Dynamsoft.Find_Mid(item)
        Child = (f"Format: {item.get_format_string()}; "
                  f"Text: {item.get_text()}; "
                  f"Mid: {mid_point}")
        box.add_child(Child)
        print(f"Barcode {item.get_text()} is inside box {box.name}")

def Export_Data(output_file):
    output_file = output_file.replace(".jpg", ".txt")
    with open(output_file, 'w') as f:
        for box in Boxes:
            f.write(str(box) + "\n")
    print(f"Boxes' data has been written to: {output_file}")
    return output_file
